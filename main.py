from mvc.controller import Controller
from mvc.model import Model
from mvc.view import View


if __name__ == '__main__':
    model = Model()
    view = View()
    controller = Controller(model=model, view=view)
    controller.start()
