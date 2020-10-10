import asyncio
import pickle

class Client():
    pdata = []

    # run the loops for async
    def run(self, message):
        self.loop = asyncio.new_event_loop()
        self.loop.run_until_complete(self.handle_server(message))
        self.loop.close()

    # close loop
    def close_client(self):
        self.loop.close()

    # command to get food available for today
    def get_food_by_day(self, day):
        message = f"GET FOOD BY DAY [{day}]"
        self.run(message)

    # command to get foodcourt data
    def get_foodcourts(self):
        message = "GET FOODCOURTS"
        self.run(message)

    # command to get promos
    def get_promos(self):
        message = "GET PROMOS"
        self.run(message)

    # command to get images for the foods for today
    def get_images(self, day):
        message = f"GET IMAGES [{day}]"
        self.run(message)

    # command to log a purchase to server
    def log_purchase(self, total_items, total_cost):
        message = f"LOG PURCHASE [{total_items},{total_cost}]"
        self.run(message)

    # handles commands and server queries
    async def handle_server(self, message):
        reader, writer = await asyncio.open_connection('localhost', 42069,
                                                    loop=self.loop)
        writer.write(message.encode())

        data = await reader.read()
        
        self.pdata = pickle.loads(data)

        if "GET IMAGES" not in message:
            print("SERVER SAYS: ", self.pdata)
        else:
            print("Received food images from server.")

        print('Close the socket')
        writer.close()