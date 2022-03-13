# Selenium is a powerful tool for controlling web browsers through programs and performing browser automation. It is
# functional for all browsers, works on all major OS and its scripts are written in various languages i.e Python,
# Java, C#, etc, we will be working with Python.
import datetime
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager

# Keeps the Selenium browser session open,
# otherwise the garbage collection in Python closes the browser.
# The browser not closing is just a preference, it also works perfect without it!
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
driver.maximize_window()

# Paste the URL of the FILLED form you want to automate in the get function.
driver.get("https://www.hochschulsport.uni-mannheim.de/angebote/aktueller_zeitraum_0/_D2FitnessGym.html")

time.sleep(1)

# Accept the cookie pop up.
accept_cookies = driver.find_element(By.XPATH, value='//*[@id="page-25673"]/div[3]/div[2]')
accept_cookies.click()

# Just in case it doesn't find the "buchen" button again, because
# it was firstly obstructed by the cookie popup.
time.sleep(1)

# Defining the possible appointments and printing them out.
appointment_options = {
    1: "09:30-11:00",
    2: "11:15-12:45",
    3: "13:00-14:30",
    4: "14:45-16:15",
    5: "16:30-18:00",
    6: "18:15-19:45",
    7: "20:00-21:30",
}

# In Python, weekday() can be used to retrieve the day of the week. The datetime.today() method returns the current
# date, and the weekday() method returns the day of the week as an integer where Monday is indexed as 0 and Sunday is 6.
current_day = datetime.datetime.today().weekday()

# Formatted to show the hours and the minutes.
current_time = datetime.datetime.now().strftime("%H:%M")

print("Hello, ma friend!\nThose are your available training sessions for today:")

# We specify one, so that we can go in the while loop, later.
# We use sets, because later, if the 1 gets added, it won't be a duplicate value.
appointment_booked_today = {1}
appointment_booked_tomorrow = {1}

# appointment_today = []
# # List with the choices available tomorrow. We will use that below for the column_index.
# appointment_tomorrow = []

# E-Mail is created here, because of scope.
email = "georgi.haydukov99@gmail.com"

# Helps to identify the index of the days
counter = 0
while not appointment_booked_tomorrow == {} and not appointment_booked_today == {}:

    # We remove them directly after, because it can happen,
    # that the option 1 is not available at the time.
    # Also, when it removes the 1's the first time it loops. we don't get
    # an error, because we use discard.
    appointment_booked_today.discard(1)
    appointment_booked_tomorrow.discard(1)

    # Print the available appointments on the current day
    for appointment_number in appointment_options.keys():

        # Checks weekdays.
        if current_day >= 4:
            # Excludes the hours that are not available on Friday, Saturday and Sunday.
            if appointment_number == 1 or appointment_number == 7:
                continue

            # Checks if you have the option to book the appointment.
            # Example - You wake up at 10:00 and want to book at 9:30.
            # This should not be possible and therefore should not be printed out.
            if current_time <= appointment_options[appointment_number][:5]:
                print(f"{appointment_number}. {appointment_options[appointment_number]}")
                # appointment_today.append(appointment_number)
                appointment_booked_today.add(appointment_number)

        # Checks working days.
        else:
            # Checks if you have the option to book the appointment.
            # Example - You wake up at 10:00 and want to book at 9:30.
            # This should not be possible and therefore should not be printed out.
            if current_time <= appointment_options[appointment_number][:5]:
                print(f"{appointment_number}. {appointment_options[appointment_number]}")
                # appointment_today.append(appointment_number)
                appointment_booked_today.add(appointment_number)

    print("\nHello again, ma friend!\nThose are your available training sessions for tomorrow:")

    # Print the available appointments on the next day
    for appointment_number in appointment_options.keys():

        # Checks what is the next day
        # current_day + 1 <= 6 is written, because if the current day is Sunday,
        # we want our program to print the available appointments of Monday and we go in the else block.
        # Checks weekdays.
        if 4 <= current_day + 1 <= 6:
            # Excludes the hours that are not available on Friday, Saturday and Sunday.
            if appointment_number == 1 or appointment_number == 7:
                continue

            # Checks if you have the option to book the appointment on the next day.
            # Example - You want to book an appointment the next day.
            # According to the rules you can do that BEFORE 22-Hours and 30 minutes from the start of the appointment.
            # If you get up at 13:00 on Saturday and want to book at 14:00 on Sunday,
            # you have to wait 1-hour and 30 minutes.
            # Otherwise, the booking is not possible because of the D2 gym rules and therefore should not be printed
            # out.
            if current_time >= appointment_options[appointment_number][6:]:
                print(f"{appointment_number}. {appointment_options[appointment_number]}")
                # appointment_tomorrow.append(appointment_number)
                appointment_booked_tomorrow.add(appointment_number)

        else:
            # Checks if you can make an appointment in the working days.
            if current_time >= appointment_options[appointment_number][6:]:
                print(f"{appointment_number}. {appointment_options[appointment_number]}")
                # appointment_tomorrow.append(appointment_number)
                appointment_booked_tomorrow.add(appointment_number)

    # Click on the chosen "buchen" button.
    buchen_button = ""

    # Variables that indicate the index of the table rows (row index) and table data (column_index).
    column_index = current_day + 1  # + 1 because td starts with 1 and not with 0
    row_index = 0

    appointment_choice = int(input("\nEnter the number of your choice: \nChoose wisely! "))

    # Setting the correct row index. It is dependent on the current day!
    # appointment_choice + 1, because the appointments in the website table start from 2.
    if appointment_choice in appointment_booked_today or appointment_choice in appointment_booked_tomorrow:
        row_index = appointment_choice + 1

    # Setting the correct column index. It is dependent on the next day!
    # + 1, because it's tomorrow.
    if appointment_choice in appointment_booked_tomorrow:
        column_index += 1

    # That gives us the second tab back.
    first_tab = driver.window_handles[0]

    # Switches to the first tab,
    # otherwise the second "buchen" button won't be found.
    # We do this. because after the first loop, we find ourselves in the second tab,
    # but we want work in the first.
    driver.switch_to.window(first_tab)

    # Click on button "buchen"
    buchen_button = driver.find_element(
        by=By.XPATH,
        value=f'//*[@id="bs_pl2B6C3849BD10"]/tbody/tr[{row_index}]/td[{column_index}]/input'
    )

    buchen_button.click()

    # Little bit of time between the loading of the two tabs.
    time.sleep(0.5)

    # That gives us the second tab back.
    second_tab = driver.window_handles[1]

    # Switches to the second tab,
    # otherwise the second "buchen" button won't be found.
    driver.switch_to.window(second_tab)

    # Second Tab Actions - Here comes also the form itself.

    # Clicks the second "buchen" or "warteliste" button in the SECOND tab,
    # depending on the number of the people, who already booked an appointment.
    buchen_or_warteliste = driver.find_element(By.XPATH, value='//*[@id="bs_form_main"]/div/div[2]/div[1]')
    buchen_or_warteliste.click()

    try:

        # Clicks on the specified gender if you don't have to wait on the waiting list (Warteliste)
        gender = driver.find_element(By.XPATH, value='//*[@id="bs_kl_anm"]/div[3]/div[2]/label[2]/input')
        gender.click()

        # If you don't have to wait on the waiting list, you don't need to be in the loop.
        break
    except NoSuchElementException:
        print("\nOops, too many participants for this appointment")
        print("Do you want to receive an E-Mail if there are available slots for this appointment?")

        choice = int(input("1 - Yes\n2 - No\nEnter the number of your choice: "))

        # Enter your email and click on button "weiter"
        if choice == 1:
            email_webelement = driver.find_element(By.XPATH, value='//*[@id="bs_form_main"]/div[3]/div[2]/input')
            email_webelement.send_keys(email)

            weiter_button = driver.find_element(By.XPATH, value='//*[@id="bs_foot"]/div[1]/div[2]/input')
            weiter_button.click()

            email_notification_confirmation_text = driver.find_element(By.CSS_SELECTOR,
                                                                       value='.bs_text_red.bs_text_big')

            # We check if we were registered in the waiting list or something went wrong.
            if email_notification_confirmation_text.text == "Ihre E-Mail Adresse wurde in unseren " \
                                                            "Benachrichtigungsservice " \
                                                            "aufgenommen.":
                print("You are successfully registered in the waiting list!")
            else:
                print("There was a problem registering you in the waiting list!")

            # If we chose to be registered in the waiting list, the script terminates on the spot,
            # and we have to wait for an E-Mail confirmation
            # Selected choice must be removed from appointment dictionary (still a list)

            quit()

        # Click on button "abbrechen"
        else:

            print("You chose not to be registered in the waiting list!\n")
            print("You can choose again: ")

            # abbrechen = cancel button
            abbrechen_button = driver.find_element(By.XPATH, value='//*[@id="btn_cancel"]')

            abbrechen_button.click()

            # We want to wait a couple of seconds, in our case 1,
            # otherwise the second abbrechen (cancel) button can't be recognised and therefore clicked.
            time.sleep(1)

            # Two times, so it can be back to the start page
            abbrechen_button = driver.find_element(By.XPATH, value='//*[@id="btn_cancel"]')
            abbrechen_button.click()

            # Removes the already selected choice, so it doesn't appear one more time to the console.
            appointment_options.pop(appointment_choice)

            # Removes the already selected choice, so it doesn't appear one more time to the set,
            # therefore not damaging the program logic. We are using the discard methode,
            # because we don't want to produce an Exception if the item could not be found in the set.
            appointment_booked_tomorrow.discard(appointment_choice)
            appointment_booked_today.discard(appointment_choice)

else:
    # If the dictionary with all the choices is empty, that means,
    # that the user ran out of options and therefore the program should terminate on the spot!
    print("\nProgram is terminating...\nYou ran out of option!")
    quit()

# Fills out the specified first name.
firstname = "Georgi"
firstname_webelement = driver.find_element(By.XPATH, value='//*[@id="BS_F1100"]')
firstname_webelement.send_keys(firstname)

# Fills out the specified last name.
lastname = "Haydukov"
lastname_webelement = driver.find_element(By.XPATH, value='//*[@id="BS_F1200"]')
lastname_webelement.send_keys(lastname)

# Fills out the specified address.
address = "Hans-Sachs-Ring 5"
address_webelement = driver.find_element(By.XPATH, value='//*[@id="BS_F1300"]')
address_webelement.send_keys(address)

# Fills out the specified ZIP Code and the city.
zip_city = "68199 Mannheim"
zip_city_webelement = driver.find_element(By.XPATH, value='//*[@id="BS_F1400"]')
zip_city_webelement.send_keys(zip_city)

# Chooses your status (College student, employee, professor etc.)
# Dropdown without visible elements.
# First we click on the dropdown, so we can see the options.
# DOWNLOAD SelectorsHub Chrome extension - in this case it is unfortunately
# not useful, because this form is really, really old :(.

# We will use Select instead.
# Identifies the dropdown with Select class
select = Select(driver.find_element(By.XPATH, value='//*[@id="BS_F1600"]'))

# Selects the value with select_by_visible_text() method.
# In our case THIS DOES NOT WORK!!! WE USE INDEXING INSTEAD!
# select.select_by_visible_text("Europe")

# We can select it by indexing - select_by_index()
select.select_by_index(5)

# We wait a bit, because after we choose our option (College student),
# another field pops up, and we need to fill in our college ID-Nr.
time.sleep(1)

# Fills out the specified college ID-Nr.
college_id = "1921382"
college_id_webelement = driver.find_element(By.XPATH, value='//*[@id="BS_F1700"]')
college_id_webelement.send_keys(college_id)

# Fills out the specified E-mail.
email_webelement = driver.find_element(By.XPATH, value='//*[@id="BS_F2000"]')
email_webelement.send_keys(email)

# Fills out the specified phone number.
phone_number = "01788825515"
phone_number_webelement = driver.find_element(By.XPATH, value='//*[@id="BS_F2100"]')
phone_number_webelement.send_keys(phone_number)

# Clicks that you accept the terms and conditions checkbox button.
terms_conditions_checkbox = driver.find_element(By.XPATH, value='//*[@id="bs_bed"]/label/input')
terms_conditions_checkbox.click()

# We wait, because the button "weiter zur Buchung" is grayed out.
time.sleep(7)

# Click on button "Weiter zur Buchung"
weiter_buchen_button = driver.find_element(By.XPATH, value='//*[@id="bs_submit"]')
weiter_buchen_button.click()

# Click on button "verbindlich buchen"
verbindlich_buchen_button = driver.find_element(By.XPATH, value='//*[@id="bs_foot"]/div[1]/div[2]/input')
verbindlich_buchen_button.click()

# At the end we have to validate that the form was successfully submitted.
get_confirmation_text = driver.find_element(By.CSS_SELECTOR, value='.h1')

# Perhaps make a Window Pop Up instead of printing it out to the console?
if get_confirmation_text.text == "Bestätigung":
    print("Booking was successful!")
else:
    print("Booking was NOT successful!")
