import asyncio
import pickle
import re
from zipfile import ZipFile
import os.path
dir_path = os.path.dirname(os.path.realpath(__file__))
# database object to handle db queries
from db import Database

# async func to handle client requests
async def handle_client(reader, writer):

    # get param in square brackets of client requests
    def get_param(inp):
        param = re.search(r"\[(.+)\]", inp)
        return param.group(1)

    # convert images needed for day menu to bytes
    def prepare_images(day):
        rows = db.get_food_by_day(day)
        img_list = []
        try:
            for row in rows:
                with open(dir_path + "/images/" + row[1], "rb") as img_file:
                    img_list.append(img_file.read())
            return img_list
        except Exception as e:
            print('Something wrong happened!')
            print(e)

    request = None
    data = "ERROR. Invalid Request. Try again."
    try:
        while request != 'quit':
            db = Database()

            request = (await reader.read(255)).decode()
            
            # handling of client requests
            if request:
                print(f"--------------------------\nCLIENT SAYS: {request}")
                if "GET FOOD BY DAY" in request:
                    day = get_param(request)
                    rows = db.get_food_by_day(day)
                    if len(rows) != 0:
                        data = rows
                elif "GET FOODCOURTS" in request:
                    rows = db.get_foodcourts()
                    if len(rows) != 0:
                        data = rows
                elif "GET PROMOS" in request:
                    rows = db.get_promos()
                    if len(rows) != 0:
                        data = rows
                elif "GET IMAGES" in request:
                    day = get_param(request)
                    rows = prepare_images(day)
                    if rows:
                        data = rows
                elif "LOG PURCHASE" in request:
                    details = get_param(request)
                    if "," in details:
                        log_details = details.split(",")
                        db.add_log(log_details[0], log_details[1])
                        data = "Log successful."

                data_send = pickle.dumps(data)
                
                print(f"Size of data: {len(data_send)}")
                writer.write(data_send)

            await writer.drain()
            writer.close()
    
    # client finishes connection
    except ConnectionResetError:
        print("Connection ended.\n")


if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.create_task(asyncio.start_server(handle_client, 'localhost', 42069))
    loop.run_forever()