# Access_Control_System

## **Project Overview**

This project uses Flask and MySQL to create a web application for managing user profiles and authentication. Administrators can manage users and ordinary users update their profiles by role-based access provided by the system. Other features include managing profile pictures, CSRF protection, and the ability to change passwords.

## **Setup Instructions**
For setting up the system,

**Step 1.** Install and open xampp, start Apache and MySQL
**![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXek5Q4GQ1RtIaLbUDrZ3yVfqmYk65tSwX7noRofsS-IfaEThdE5uOiXm_tWh8LZN7JYtFY-ppA_VVmm781NTr26dpMPsjcvhq6ZxCfCaLshkeEW0M1msLYi_sXwnRsT_wq_w2X6mQ?key=I2PLTqOWb3R5hkTlqteTtx4h)**

**Step 2.** Import the adet_user database using [http://localhost/phpmyadmin/index](http://localhost/phpmyadmin/index) or through the CLI interface of mysql
**![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXdm_tDa9FQorTt0tZ5GzAsbj1J00mjF7YsbqfmjldKKa5g_G8ZafEvscjrpzfEHPO_W58SOsyC6sHrJvMzkqxyN7K8cUXXyxeRvoPGlFNAzy1STwtoB_kcNMItyRH33oAI-qS2znw?key=I2PLTqOWb3R5hkTlqteTtx4h)**

**Step 3.** Use any IDE that is able to utilize folders, for this we can use VSCode, Click on files then open folder, locate the folder that contains app.py and its local files. This is important for uploading files to the *static/uploads/profile_pics/* folder

**![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXePrUPMe-NMdyFHzK-ZKNTCQtNKE9Vo7MHi2cI7Bpt3UbyM7OY396n7FpHqz1IRiAqmQeoSqQ-St1UbnvdwtrsnTQ8UcdWAFDEffSaBNcIByr5RudqgIDwdUWQN-_s4KQkhAKOqjg?key=I2PLTqOWb3R5hkTlqteTtx4h)**

**Step 4.** Installing dependencies, we can use the terminal in VSCode to install the required dependencies. Make sure to have the requirements.txt file in the same folder. Type this command in the terminal or cmd under the same file location `pip install -r requirements.txt`

**Step 5.** Run the app.py and open this link [http://127.0.0.1:5000](http://127.0.0.1:5000)
## User Guide
To enter admin dashboard, enter the following credentials:

Email: test@gmail.com

Password: test

The admin dashboard contains all information of all users
The admin dashboard contains the ability to;

-   Add users by pressing the top left button
    
-   Sort users by pressing the roles on the top right buttons
    
-   Edit information by pressing the edit icon button
    
-   Delete Accounts by pressing the delete button
    
-   Logout session
 
To enter regular user, create an account first in the registration page
Enter the credentials to enter the dashboard
The dashboard contains:

-   User information
    
-   User profile picture
    
-   Edit button
    
-   Logout session

**Troubleshooting**

If the profile picture is not updating, make sure that the IDE is using the folder then running the app.py

If the user forgot their password, they can press the forgot button and enter their email address or update it in the admin dashboard.

The database is required for the app.py to run properly
