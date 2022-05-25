from booking.booking import Booking

# try:
#     with Booking(teardown=True) as bot: # will exit
#     # with Booking() as bot:   # browser remains open
#         bot.land_first_page()
#         bot.change_currency(currency=input("Select your currency: GEL,EUR,USD,GBP ... ").upper())
#         bot.select_place_to_go(input("Where do you want to go? ").strip())
#         bot.select_dates(
#             check_in_date=input("Enter Check in date Exc: 2022-05-25: "),
#             check_out_date=input("Enter Check out date Exc: 2022-05-27: "))
#         bot.select_adults(int(input("Select adults number: ").strip()))
#         bot.click_search()
#         bot.apply_filtrations()
#         bot.refresh() # A workground to let our bot to grab the data properly
#         bot.report_result()

# except Exception as e:
#     if 'in PATH' in str(e):
#         print(
#             'You are trying to run the bot from command line \n'
#             'Please add webdriver in the selenium_booking directory \n'
#             'Linux: \n'
#             '    PATH = "selenium_booking/chromedriver" \n'
#         )
#     else:
#         raise
with Booking(teardown=True) as bot: # will exit
    bot.land_first_page()
    bot.change_currency(currency=input("Select your currency: GEL,EUR,USD,GBP ... ").upper())
    bot.select_place_to_go(input("Where do you want to go? ").strip())
    bot.select_dates(
            check_in_date=input("Enter Check in date Exc: 2022-05-25: "),
            check_out_date=input("Enter Check out date Exc: 2022-05-27: "))
    bot.select_adults(int(input("Select adults number: ").strip()))
    bot.click_search()
    bot.apply_filtrations()
    bot.refresh() # A workground to let our bot to grab the data properly
    bot.report_result()