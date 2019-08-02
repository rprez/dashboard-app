from app import ute_dashboard

application = ute_dashboard.app.server
application.logger.info("Start gateway-cuenca-piot")

if __name__ == '__main__':
    application.run()
