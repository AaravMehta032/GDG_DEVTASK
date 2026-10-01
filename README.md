# GDG_DEVTASK
A Python 3-based URL shortener that generates unique, randomly generated codes for URLs and allows users to save, view, and delete them.
The program has 4 main functionalities:
1. Shorten a URL: Enter 1 to enter a URL to be shortened. The URL must start with http:// or https://.
2. View existing records: Enter 2 to view the existing URL records, including the original URLs, their assigned codes, and their shortened URLs in JSON format.
3. Delete a URL: Enter 3 to delete a URL by entering its original URL, assigned code, or shortened URL.
4. Exit: Enter 4 to exit the program.

The program automatically creates and updates a urls.json file, which stores the original URLs and their assigned codes.

The base URL used by the shortener is: https://sho.rt/
Each URL is assigned a unique alphanumeric code, which is appended to the base URL to create the shortened URL.
