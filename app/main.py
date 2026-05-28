def main():
    from app.core.config import garantir_diretorios
    from app.services.config_service import ConfigService
    from app.services.print_queue_service import PrintQueueService
    from app.controllers.app_controller import AppController
    from app.views.main_view import MainView

    garantir_diretorios()

    config_service = ConfigService()
    queue_service = PrintQueueService()

    controller = AppController(config_service, queue_service)

    import sys
    view = MainView(controller)
    controller.set_view(view)
    try:
        view.mainloop()
    except KeyboardInterrupt:
        print("\nEncerrado pelo usuário (Ctrl+C)")
        sys.exit(0)
