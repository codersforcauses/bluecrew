# Staff Documentation

## Admin Accounts

There are two user types: admin users and non-admin users.

Non-admin users:

* Interact with the web app as a typical user.

Admin users:

* Will not have a visible profile, and will not be visible on the leaderboard or in friend searches.

* Will have access to the admin dashboard.

* Will have access to the admin page to select active bingo grid challenges.

## Admin Dashboard

The admin dashboard is used to manage users, bingo grid challenges, and submissions. The admin dashboard can be found at https://blingo.codersforcauses.org/admin/ and all accounts with admin privileges will be able to access it. The initial admin user login details can be located in the Handover Document.

### Navigation

Upon logging in, you will be greeted with the following dashboard.

![Screenshot](img/admin-dashboard-overview.png)

All tables from that are stored into the database used for the functionality of the website can be seen here. Not all sections will be relevant. In particular, anything under the `DJANGO Q` header can be ignored.

### Creating New Admin Accounts

1. Navigate into the Users dashboard by clicking `Users` under the BINGO header.

![Screenshot](img/create-new-admin.png)

2. Click `ADD USER` in the top right.

3. Fill in the `Username`, `Email`, and `Password` fields. All other fields may be left blank.

4. Tick the `Superuser status` box to enable admin privileges.

![Screenshot](img/new-admin-fields-1.png)

![Screenshot](img/new-admin-fields-2.png)

5. Click `SAVE` to create the new user

Alternatively, if you would like to give an existing user admin privileges, select the user from the user list, tick the `Superuser status` box, and click `SAVE`.

## User Management

The details of both admin and non-admin users may be accessed and edited by clicking the username of the user.

## The Bingo Grid

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

## Challenges

To view the database of challenges, click on the "Challenges" tab on the left. You will then be presented with a list of the challenges that have been created so far.

![Screenshot](img/view-challenges.png)

To create a new challenge, press the "Add Challenge" button in the top right. You can view and/or edit the details of an existing challenge by clicking on that challenge in the list of challenges. This will bring you to a form with the ability to view/modify the name, description, type, and point-value of the challenge. The challenge's ID and total number of completitions by users playing the bingo game is also displayed.

![Screenshot](img/edit-challenge.png)

To delete one or more challenges, mark the checkboxes next to the challenges you want to delete, select "Delete selected challenges" from the dropdown menu, and press the "Go" button.

![Screenshot](img/delete-challenge.png)

## User Submissions

### Viewing submissions

### Revoking submissions
