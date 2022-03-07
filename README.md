# Online gym form Automation

A python script used to automate an online form of my local university gym in Germany.

P.S The website form is in German, that's why the button names are also in German.

1. The script starts with installing Chrome Driver.

2. It then opens the URL of the booking form of the local university.

3. The gym appointments are shown and the user can choose one of them.

4. If the appointment is available, the script proceeds with entering the form, if not, the user has a choice to be
   enlisted in the waiting list or to go back and choose another appointment. If the user chooses to be registered in
   the waiting list, the program terminates and the user has to wait for a confirmation E-Mail, which will be sent if
   there is an available slot. Otherwise, the script proceeds with step 6.

6. The script then fills the necessary fields.

7. At the end a confirmation message is being printed out in the console, signaling that the booking was successful.
