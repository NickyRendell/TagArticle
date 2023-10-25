import json

# Replace this with your actual JSON string
json_text = json_text = """ [{"id":154547,"title":{"rendered":"Respected duo stand forward to lead Venstre"},"excerpt":{"rendered":"Troels Lund Poulsen and Stehpanie Lose are now official candidates to take the helm of Venstre. The duo is expected 
to be officially elected in November  \t\t<div class=\"woocommerce\">\n\t\t\t<div class=\"woocommerce-info wc-memberships-restriction-message wc-memberships-message wc-memberships-content-restricted-message\">\n\t\t\t\t\n<div class=\"wp-block-group paywall_login is-layout-flow wp-block-group-is-layout-flow\"><div class=\"wp-block-group__inner-container\">\n<hr class=\"wp-block-separator has-text-color has-black-color has-alpha-channel-opacity has-black-background-color has-background is-style-wide\" \/>\n\n\n\n<h2 class=\"wp-block-heading\">Full version of this article is only available to subscribers.<\/h2>\n\n\n\n<p><strong>Already a subscriber, sign in here:<\/strong><\/p>\n\n\n<div class=\"logged-out wp-block-button__link wp-element-button btn wp-block-loginout\"><a rel=\"nofollow\" href=\"https:\/\/cphpost.dk\/wp-login.php?redirect_to=https%3A%2F%2Fcphpost.dk%2Fwp-json%2Fwp%2Fv2%2Fposts%3Fpage%3D1%26_fields%3Did%2Ctitle%2Cexcerpt\">Log in<\/a><\/div>\n\n\n<div>\n\t<p class=\"woocommerce-LostPassword lost_password\">\n\t\t<a href=\"https:\/\/cphpost.dk\/my-account\/lost-password\/\">Lost your password?<\/a>\n\t<\/p>\n<\/div>\n\n<\/div><\/div>\n\n\n\n<hr class=\"wp-block-separator has-text-color has-black-color has-alpha-channel-opacity has-black-background-color 
has-background is-style-wide"""


# Replace invalid escape sequences
fixed_json_text = json_text.replace('\/', ' ')

# Parse the JSON
try:
    data = json.loads(fixed_json_text)
    print(data)
except json.JSONDecodeError as e:
    print('Failed to parse JSON:', e)
# Example usage:
