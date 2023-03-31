import tkinter as tk
import pika

class Application(tk.Frame):
    def __init__(self, master, middleware_host):
        super().__init__(master)
        self.master = master
        self.middleware_host = middleware_host
        self.create_widgets()
        self.setup_messaging()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.master, width=500, height=500, bg='white')
        self.canvas.pack(side='left', fill='both', expand=True)

        self.query_label = tk.Label(self.master, text='Query person:')
        self.query_label.pack(side='top')

        self.query_entry = tk.Entry(self.master)
        self.query_entry.pack(side='top')

        self.query_button = tk.Button(self.master, text='Search', command=self.query_person)
        self.query_button.pack(side='top')

        self.contacts_label = tk.Label(self.master, text='Contacts:')
        self.contacts_label.pack(side='top')

        self.contacts_listbox = tk.Listbox(self.master)
        self.contacts_listbox.pack(side='top', fill='both', expand=True)

    def setup_messaging(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.middleware_host))
        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange='position', exchange_type='fanout')
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.queue_name = result.method.queue
        self.channel.queue_bind(exchange='position', queue=self.queue_name)

        self.channel.exchange_declare(exchange='query', exchange_type='topic')
        self.result = self.channel.queue_declare(queue='', exclusive=True)
        self.response_queue_name = self.result.method.queue
        self.channel.queue_bind(exchange='query-response', queue=self.response_queue_name)

        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.update_environment, auto_ack=True)
        self.channel.basic_consume(queue=self.response_queue_name, on_message_callback=self.update_contacts, auto_ack=True)
        self.channel.start_consuming()

    def update_environment(self, channel, method, properties, body):
        # Parse the position message and update the canvas
        x, y, name = body.decode().split(',')
        x, y = int(x), int(y)
        color = 'red' if name == self.query_entry.get() else 'blue'
        self.canvas.create_rectangle(x*50, y*50, x*50+50, y*50+50, fill=color)

    def update_contacts(self, channel, method, properties, body):
        # Parse the query-response message and update the contacts listbox
        contacts = body.decode().split(',')
        self.contacts_listbox.delete(0, tk.END)
        for contact in reversed(contacts):
            self.contacts_listbox.insert(0, contact)

    def query_person(self):
        # Publish a query message for the specified person
        person = self.query_entry.get()
        self.channel.basic_publish(exchange='query', routing_key=person, body='')

    def close(self):
        # Close the messaging connection
        self.connection.close()

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root, 'localhost')
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()

