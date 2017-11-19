from woocommerce import API as WoocommerceAPI

class Faviosmom_wc:
    wcapi = WoocommerceAPI(
        url="http://faviosmom.com",
        consumer_key="ck_07255729fa6f3226ec93dbf0715f43c802679da9",
        consumer_secret="cs_ad44500a974ab6f3d268a0ac235f11193a352aa4",
        api="wp-json",
        wp_api=True,
        timeout=15,
        version="wc/v2"
    )

