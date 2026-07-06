from utils.logger import logger


class NetworkHelper:

    @staticmethod
    def block_images(page):

        logger.info("Blocking image requests")

        page.route(
            "**/*.{png,jpg,jpeg,gif,svg,webp}",
            lambda route: route.abort()
        )

    @staticmethod
    def block_css(page):

        logger.info("Blocking CSS")

        page.route(
            "**/*.css",
            lambda route: route.abort()
        )

    @staticmethod
    def unblock_all(page):

        logger.info("Removing all routes")

        page.unroute_all()


    @staticmethod
    def mock_employee_api(page):

        logger.info("Mocking employee API")

        page.route(
            "**/api/v2/pim/employees**",
            lambda route: route.fulfill(
                status=200,
                content_type="application/json",
                body="""
                {
                    "data":[
                        {
                            "employeeId":"EMP999",
                            "firstName":"Mock",
                            "lastName":"Employee"
                        }
                    ]
                }
                """
            )
        )

    @staticmethod
    def mock_server_error(page):

        logger.info("Returning mocked 500 response")

        page.route(
            "**/api/**",
            lambda route: route.fulfill(
                status=500,
                body="Internal Server Error"
            )
        )

    @staticmethod
    def simulate_offline(page):

        logger.info("Simulating offline mode")

        page.context.set_offline(True)

    @staticmethod
    def restore_network(page):

        logger.info("Restoring network")

        page.context.set_offline(False)