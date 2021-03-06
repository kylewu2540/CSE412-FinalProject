
#!/usr/bin/env python3
"""
Created on Mon Mar 14 13:51:45 2022
Updated on Sun Apr 24 04:53:00 2022
Written by Jake Kenny, Ryan Rademacher, Victor Ruiz, Kyle Wu
"""

from tkinter.constants import INSERT
import PySimpleGUI as sg
import sys
import psycopg2 as pg
import random 



"""creates the tables with attributes and constraints  """

create_db = '''CREATE database musicDB '''
create_song = '''CREATE TABLE IF NOT EXISTS "song" (
                    songID  integer PRIMARY KEY,
                    Title   varchar(40) NOT NULL,
                    ArtistID    integer REFERENCES artist(ArtistID),
                    runTimeSeconds  integer, 
                    genres  varchar(20), 
                    artistName  varchar(20) NOT NULL 
                    )'''
create_users = ''' CREATE TABLE IF NOT EXISTS "users" (
                    UserID  integer PRIMARY KEY,
                    fname   varchar(20) NOT NULL, 
                    lname   varchar(20) NOT NULL, 
                    username varchar(40) NOT NULL, 
                    userPass    varchar(50) NOT NULL
                     
                    )'''
create_artist = ''' CREATE TABLE IF NOT EXISTS "artist" (
                    ArtistID  integer PRIMARY KEY,
                    fname   varchar(20) NOT NULL, 
                    lname   varchar(20) NOT NULL
                    
                    )'''

create_album = ''' CREATE TABLE IF NOT EXISTS "album" (
                    AlbumID  integer PRIMARY KEY,
                    albumName   varchar(40) NOT NULL, 
                    artistName   varchar(20) NOT NULL, 
                    releaseYear    DATE, 
                    genres      varchar(20)
                    
                    )'''
create_rating = '''CREATE TABLE IF NOT EXISTS "rating" (
                    songID integer,
                    FOREIGN KEY(songID) REFERENCES song(songID),                   
                    avgRating integer
                   
                  
                    )'''

create_favorites = ''' CREATE TABLE IF NOT EXISTS "favorites" (
                    songID integer, 
                    userID integer,
                    PRIMARY KEY (songID, userID),
                    FOREIGN KEY(songID) REFERENCES song(songID),
                    FOREIGN KEY (userID) REFERENCES users(userID),
                    listID  integer 
                   )'''

create_makes = '''CREATE TABLE IF NOT EXISTS "artistalbum" (
                AlbumID integer,
                ArtistID integer, 
                PRIMARY KEY(AlbumID, ArtistID),
                FOREIGN KEY (AlbumID)  REFERENCES album(AlbumID),
                FOREIGN KEY(ArtistID) REFERENCES artist(ArtistID)
                )'''

create_song_album_relation = '''CREATE TABLE IF NOT EXISTS "albumsongrelation"(
                            AlbumID integer, 
                            songID  integer, 
                            PRIMARY KEY(AlbumID, songID),
                            FOREIGN KEY(AlbumID) REFERENCES album(AlbumID),
                            FOREIGN KEY(songID) REFERENCES song(songID)
                            )'''


"""CREATE MUSICDB"""

"""cur.execute(create_db)"""




"""cur.execute(create_artist)
cur.execute(create_song)
cur.execute(create_users)
cur.execute(create_album)
cur.execute(create_favorites)
cur.execute(create_makes)
cur.execute(create_song_album_relation)

"""

insert_userinfo_query= "INSERT INTO users (userid, fname, lname, username, userpass) VALUES (%s,%s, %s, %s, %s)"
userData = [('14589652', 'Johnny', 'Smith', 'johnS11', '3242cDsx#@'),
            ('34738040', 'Bradly',  'Johnson', 'bradJ23', 'b2dkd0x11'),
            ('78568904', 'Charlie', 'Valentine', 'charVin15','349dcdlsxx#@'),
            ('75489203', 'Doug', 'Alson', 'dougAls19','98985vbdxk#)(2)'),
            ('23942123', 'Ernesto', 'Lopez', 'elopz53','fdj04894!!@@'),
            ('53982832', 'Xavier', 'Rivers','xriver55','bndf2$%$%')]


insert_artistalbum_info_query = "INSERT INTO album (albumid, albumname, artistname, releaseyear, genres) VALUES (%s, %s, %s, %s, %s)"
albumData = [('604','The Brave','Adam Calhoun','18-Feb-22','Hip Hop'),
             ('718','As I Am','Alicia Keys','10-Sep-07', 'R&B'),
             ('643','Yours Truly','Arianna Grande','26-Mar-13', 'R&B'),
             ('867','Callaita','Bad Bunny','31-May-19', 'Reggaeton'),
             ('929','13 Reasons Why','Billie Eilish','19-Apr-18', 'Pop'),
             ('213','Black Out','Britney Spears','31-Aug-07', 'Dance Pop'),
             ('625','Unorthodox Jukebox','Bruno Mars','1-Oct-12', 'Pop Rock'),
             ('654','Romance','Camila Cabello','21-Jun-19', 'Latin Pop'),
             ('835','Invasion of Privacy','Cardi B','4-Apr-18','Hip Hop'),
             ('248' ,'F.A.M.E','Chris Brown','25-Apr-10','Dance Pop'),
             ('925','Starting Over','Chris Stapleton','28-Apr-20','Country'),
             ('491','Listen','David Guetta','16-Mar-15','Trap'),
             ('793','Demi','Demetria Lovato','25-Feb-13','Electric Pop'),
             ('152','Jolene','Dolly Parton','15-Oct-73', 'Country'),
             ('540','Future Nostalgia','Dua Lipa','1-Oct-20','Electric Pop'),
             ('910','Shape of you','Ed Sheeran','6-Jan-07','Pop'),
             ('801','Honky Chateau','Elton John','17-Apr-72', 'Pop'),
             ('597','Goldmin','Gabby Barrett','29-Jul-19','Country'),
             ('206','Four','Harry Styles','14-Nov-14','Folk Pop'),
             ('380','2014 Forrest Hills Drive','J Cole','9-Dec-14','Hip Hop'),
             ('390','Thats what they say','Jack Harlow','9-Dec-20', 'Hip Hop'),
             ('358','My kinda party','Jason Aldean','4-Apr-11', 'Country'),
             ('454','Love?','Jennifer Lopez','8-Feb-11','Dance Pop'),
             ('399', 'My World 2.0', 'Justin Bieber', '18-Jan-10','Pop')]

insert_artist_info_query = "INSERT INTO artist (artistid, fname, lname) VALUES (%s, %s, %s)"
artistData = [('36105', 'Adam', 'Calhoun'),
              ('8355', 'Alicia', 'Keys'), 
              ('39021', 'Arianna', 'Grande'),
              ('46023','Bad','Bunny'),
              ('51310', 'Billie', 'Eilish'),
              ('35448','Britney','Spears'),
              ('83033','Bruno','Mars'),
              ('39277','Camila','Cabello'),
              ('97838','Cardi','B'),
              ('67572','Chris','Brown'),
              ('59369','Chris','Stapleton'),
              ('37563','David' ,'Guetta'),
              ('76689','Demetria','Lovato'),
              ('58312','Dolly','Parton'),
              ('40735','Dua','Lipa'),
              ('67172','Ed','Sheeran'),
              ('86863','Elton','John'),
              ('54082','Gabby' ,'Barrett'),
              ('53425','Harry','Styles'),
              ('29103','J','Cole'),
              ('3068','Jack','Harlow'),
              ('54883','Jason','Aldean'),
              ('97437','Jennifer','Lopez'),
              ('22358','Justin','Bieber')]

insert_songinfo_query = "INSERT INTO song (songid, title, artistid, runtimeseconds, genres, artistname) VALUES (%s, %s, %s, %s, %s, %s)"
data =[('5010', 'Dont wanna hear it', '36105', '183', 'Hip Hop', 'Adam Calhoun'),
       ('6732', 'No one', '8355', '254', 'R&B', 'Alicia Keys'),
       ('9222','The Way' ,'39021','190','R&B','Arianna Grande'),
       ('6752','Callaita','46023','251','Reggaeton','Bad Bunny'),
       ('7833','Lovely','51310','200','Pop','Billie Eilish'),
       ('7246','Gimmie More','35448','251','Dance pop','Britney Spears'),
       ('9009','Locked out of heaven','83033','233','Pop rock','Bruno Mars'),
       ('7393','Senorita','39277','190','Latin Pop','Camila Cabello'),
       ('9583','Drip','97838','263','Hip Hop','Cardi B'),
       ('8014','Yeah 3x','67572','241','Dance pop','Chris Brown'),
       ('9049','Starting Over','59369','240','Country','Chris Stapleton'),
       ('9616','Hey Mama','37563','192','Trap','David Guetta'),
       ('9243','Heart Attack','76689','210','Electric Pop','Demetria Lovato'),
       ('5363','Jolene','58312','162','Country','Dolly Parton'),
       ('6999','Levitating','40735','203','Electric Pop','Dua Lipa'),
       ('8421','Shape of you','67172','233','Pop','Ed Sheeran'),
       ('9156','Rocket Man','86863','281','Rock','Elton John'),
       ('9296','I Hope','54082','210','Country','Gabby Barrett'),
       ('5203','Night Changes','53425','227','Folk Pop','Harry Styles'),
       ('7480','Apparently','29103','293','Hip Hop','J Cole'),
       ('6979','Way out','3068','169','Hip Hop','Jack Harlow'),
       ('9810','Dirt Road Anthem','54883','330','Country','Jason Aldean'),
       ('9990','On the Floor','97437','284','Dance pop','Jennifer Lopez'),
       ('8121','Baby','22358','216','Pop','Justin Bieber')]

insert_songrating_query = "INSERT INTO rating (avgrating, songid) VALUES (%s, %s)"
ratingData = [('2','5010'),
              ('1','6732'),
              ('4','9222'),
              ('5','6752'),
              ('0','7833'),
              ('0','7246'),
              ('0','9009'),
              ('0','7393'),
              ('0','9583'),
              ('0','8014'),
              ('0','9049'),
              ('0','9616'),
              ('0','9243'),
              ('0','5363'),
              ('0','6999'),
              ('0','8421'),
              ('0','9156'),
              ('0','9296'),
              ('0','5203'),
              ('0','7480'),
              ('0','6979'),
              ('0','9810'),
              ('0','9990'),
              ('0','8121')]

insert_userfavorites_query = "INSERT INTO favorites (songid, userid, listid) VALUES (%s,%s, %s)"
favoritesData = [('5010', '14589652', '000453'),
                 ('6732', '14589652','000453'),
                 ('9810','14589652', '000453')]

insert_makesrelation_query = "INSERT INTO artistalbum (albumid, artistid) VALUES (%s, %s)"
makesData= [('718','8355'),
            ('491', '37563')]

insert_songalbum_query= "INSERT INTO albumsongrelation (albumid, songid) VALUES (%s, %s)"
songalbumData = [('910','8421'),
                 ('358','9810')]





"""INSERT DATA"""
"""
cur.executemany(insert_artist_info_query, artistData)
cur.executemany(insert_artistalbum_info_query, albumData)
cur.executemany(insert_songinfo_query, data)
cur.executemany(insert_userinfo_query, userData)

cur.executemany(insert_userfavorites_query, favoritesData)
cur.executemany(insert_makesrelation_query, makesData)
cur.executemany(insert_songalbum_query, songalbumData)
"""






#Temp login dictionary. Will be replaced with a SQL database
accounts = {'Admin':'123456'}
def rate_song(songName, rateValue):

    cur.execute("SELECT title, songid FROM song")
    song = cur.fetchall()
    songFound = ""
    found = False
    
    for i in song:

        if i[0] == songName:
            found = True
            songFound = i[1]
    
    if found:

        cur.execute("UPDATE rating SET avgrating =%s WHERE songid = %s",(rateValue, songFound))
        con.commit()
        sg.Popup("Song Successfully Rated !\n")
    else:
        sg.Popup("Song could not be found ")
    
    #print(favorites)
    



def create_rate_window():
    rate_layout = [
        [sg.Text("Which Song do you Want to Rate?"), sg.InputText()], 
        [sg.Text("Rate 1-5 : "), sg.InputText()],
        [sg.Button("Rate Song")]
        
        ]
    rate_window = sg.Window("Rate Song ", rate_layout, margins = (100,50))
    return rate_window

def create_login_window():
    login_layout = [
        [sg.Text("Please enter your username and password, or create an account")], 
        [sg.Text("Username: "), sg.InputText()],
        [sg.Text("Password: "), sg.InputText(password_char = '*')],
        [sg.Button("Log In")],
        [sg.Button("Create Account")]
        ]
    login_window = sg.Window("CSE 412 Project", login_layout, margins = (100,50))
    return login_window

def create_incorrect_login_window():
    incorrect_login_layout = [
        [sg.Text("Incorrect Username or Password")],
        [sg.Button("OK")]
        ]
    incorrect_login_window = sg.Window("CSE 412 Project", incorrect_login_layout, margins = (50, 25))
    return incorrect_login_window

def create_create_account_window():
    create_account_layout = [
       [sg.Text("Username: "), sg.InputText()],
       [sg.Text("First Name: "), sg.InputText()],
       [sg.Text("Last Name: "), sg.InputText()],
       [sg.Text("Password: "), sg.InputText(password_char = '*')],
       [sg.Button("Create Account")]
       ] 
    create_account_window = sg.Window("CSE 412 Project", create_account_layout, margins = (100, 50))
    return create_account_window
  
#The music library UI is composed of the library and favorites tab
#These two tabs are very similar; the only difference is that the table in favorites is a subset of the table in library
def create_library_UI(username, libSort, favSort):

    #Taking data from database to put into application
    #implement sorting system in library so user can sort by song, length, genre, artist, album, releasedate, rating
    #by changing the libSort tag and having appropriate changes in sg.Table / libVal
    #Library window

    cur.execute("SELECT song.title, song.runtimeseconds, song.genres, song.artistname, album.albumname, album.releaseyear, rating.avgrating" +
               " FROM song LEFT JOIN albumsongrelation as albumrel on song.songid = albumrel.songid LEFT JOIN album on album.albumid = albumrel.albumid" +
               " LEFT JOIN rating on song.songid = rating.songid ORDER BY " + libSort + " ASC")
    libVal = cur.fetchall()

    #Favorite window to display current users favorites
    #some tab commented code below is used if an error starts to occur from username not being recognized
        #favCheck = True
        #try:
    cur.execute("SELECT song.title, song.runtimeseconds, song.genres, song.artistname, album.albumname, album.releaseyear, rating.avgrating" +
                   " FROM song LEFT JOIN albumsongrelation as albumrel on song.songid = albumrel.songid LEFT JOIN album on album.albumid = albumrel.albumid" +
                   " LEFT JOIN rating on song.songid = rating.songid LEFT JOIN favorites on song.songid = favorites.songid" +
                   " LEFT JOIN users on favorites.userid = users.userid WHERE users.username = \'" + username + "\' ORDER BY " + favSort + " ASC")
        #except:
        #    print("favCheck = False")
        #    favCheck = False

        #if(favCheck):
    favVal = cur.fetchall()
        #else:
        #    favVal = [[0, 0, 0, 0, 0, 0, 0]]

    #libVal = [[0],[1],[2],[3],[4],[5],[6]]
    #adding data into application
    library_layout = [
        [sg.Text("Add Song Name to Favorites: "), sg.InputText(), sg.Button("Submit")],
        [sg.Text("Sort By: "), sg.Button("Song"), sg.Button("Length"), sg.Button("Genre"), sg.Button("Artist"), sg.Button("Album"), sg.Button("Year"), sg.Button("Rating"), sg.Button("Rate Song")],
        [sg.Table(values = libVal, headings = ['Song', 'Length', 'Genre', 'Artist', 'Album', 'Year', 'Rating'])]
        ]
    favorites_layout = [
        [sg.Text("Remove Song Name from Favorites: "), sg.InputText(), sg.Button("Remove ")],
        [sg.Text("Sort By: "), sg.Button("Song"), sg.Button("Length"), sg.Button("Genre"), sg.Button("Artist"), sg.Button("Album"), sg.Button("Year"), sg.Button("Rating")],
        [sg.Table(values = favVal, headings = ['Song', 'Length', 'Genre', 'Artist', 'Album', 'Year', 'Rating'])]
        ]
    tabgrp = [
        [sg.TabGroup([
            [sg.Tab('Library', library_layout, key = '-LIBRARY_TAB-')],
            [sg.Tab('Favorites', favorites_layout, key = '-FAVORITES_TAB-')]
            ], key = '-TABGRP-')]
        ] 
    library_UI_window = sg.Window("CSE 412 Project", tabgrp).finalize()
    #library_UI_window.maximize()
    library_UI_window['-TABGRP-'].expand(True, True)
    return library_UI_window

#Returns 0 on an unsuccessful login, 1 on a successful login, and 2 if the user wants to create an account
#Parameters: the provided username, the provided password, the login window, the login window's event handler
#I made the event handler a parameter to avoid creating multiple event handlers for the same window
def login(username, password, login_window, event):
    cur.execute("SELECT userid, fname, username, userpass FROM users")
    users = cur.fetchall()
    success = False
    for i in users:
        if username == i[2] and password == i[3]:
            #print("username and password match!")
            sg.Popup("Login Success!")
            success = True
            return 1
           #open window after successful login
    
    
    if event == "Create Account":
        login_window.close()
        create_account()
        

    if success == False:
        sg.Popup('Login Failed!')
        #print("login failed!\n")
        return 0



     
#Inserts the username and password as a key-vakue pair in accounts
#This should eventually interact with an SQL database, not a Python dictionary            
def create_account():
    create_account_window = create_create_account_window()
    event, values = create_account_window.read()
    if event == "Create Account":
        #TODO: Replace the following line of code with an SQL command to add the username and password to the database
        accounts[values[0]] = values[1]
        random_num = random.randint(10000000,99999999)
        """the %s are the values that that will be passed through the username_pass_data"""
        insert_username_pass = "INSERT INTO users (userid ,username, fname, lname,  userpass) VALUES (%s,%s,%s, %s, %s)"
        username_pass_data = [(random_num, values[0], values[1],values[2],values[3])]
        cur.execute("SELECT userid, fname, username, userpass FROM users")
        """in order to check all the entries have to execute the cur.execute query"""
        """using fetchall i can then loop through each column value checking for matching username or userid"""
        """if theres a match then abort back to main otherwise commit the query """

        users = cur.fetchall()
        exists = False
        
        for i in users:
            if(values[0] == i[2]):
                user = values[0]
                #print("Username exists!\n")
                sg.Popup('Username already exists!')
                exists = True
                create_account_window.close()
                main()
            elif random_num == i[0]:
                #print("Same ID exists!\n")
                sg.Popup('Same ID already exists!')
                exists = True
                create_account_window.close()
                main()
 


        if exists == False:
                cur.executemany(insert_username_pass,username_pass_data)
                con.commit()
                sg.Popup('Account Successfully Created!')
                #print("Account Successfully Created!\n")
                create_account_window.close()
                main()
       

#this function uses user_id (user) as an argument and song name (value)
#to determine the song is within the user's favorite's list
# if not, it returns false and an error message will print 
#if so, it returns true and a pop will indicate the user's song has been sucessfully removed from their favorites list
#this function first uses a sql query to grab the favorites for this particular user
#then we call another sql query to select all songid's and titles from the song table
#we are able to delete the song if we find a match
def remove_from_favorites(value, user):

    operation = False
    #delete_song_toFavorites = "DELETE FROM FAVORITES WHERE songid = %s"
    #cur.executemany(delete_song_toFavorites,value)
    #con.commit()
    #print(user)
    cur.execute("SELECT * FROM Favorites WHERE userid = %s", (user, ))
    song_list = cur.fetchall()

    #print(song_list)

    cur.execute("SELECT songid, title FROM song")

    song_val = cur.fetchall()

    #print(value)

    tmp = 0
    #print(song_val[0], "\t0")
    #print(song_val[1], "\t1")

    #print(song_val[1][0])

    for i in song_val:
        #print(i)
        if i[1] == value:
            #print(value)
            tmp = i[0]
            #print(tmp)

    #print(tmp)

    for j in song_list:
        if(j[0] != tmp):
            operation = True

    delete_song_toFavorites = "DELETE FROM FAVORITES WHERE songid = %s AND userid = %s"
    song = [(tmp, user)]
    cur.executemany(delete_song_toFavorites, song)
    con.commit()
    #print("we are here after the delete query")

    if operation == True: #there's no duplicate here
        #print("alright, we reached here")
        return True

    return False       
            
  

def main():
    global con,cur
   
    operation = False
    con = pg.connect(host="localhost", user="postgres", password="412group", dbname="musicdb")
    cur = con.cursor()
    con.autocommit= True
    login_window = create_login_window()
    event, values = login_window.read()
   
    sign_on = login(values[0], values[1], login_window, event)
    user = values[0] #variable used for create_library_UI favorites
    libSort = "title" #variable used for create_library_UI sorting
    favSort = "title" #variable used for create_library_UI sorting
    rateValue = 0
    #cur.execute(create_rating)
    #cur.executemany(insert_songrating_query, ratingData)
    #stay on main screen when login fails 
    while sign_on == 0:
         if event == sg.WIN_CLOSED:
             sys.exit()

         try:
            login_window.close()
         except:
            print("window not made yet (only happens on first entering sign_on == 0 loop)")

         login_window = create_login_window()
         event, values = login_window.read()
         sign_on = login(values[0], values[1], login_window, event)
         
    #open and stay on libary window when login successful
    while sign_on == 1:
        login_window.close()
        songFound =" "
        userID =" "
        random_num = 0
        try:
            library_window.close()
        except:
            print("window not made yet (only happens on first entering sign_on == 1 loop)")

        library_window = create_library_UI(user, libSort, favSort,) #create display and sort
        event, values = library_window.read()

        #listen for events of library_window.read():

        #very useful print values to understand what is going on in the sign_on == 1 loop
        #print(event)
        #print(values)

        #exit event
        if event == sg.WIN_CLOSED:
            cur.close()
            con.close()
            sys.exit()

        #change sorting of library window based on button press for create_library_UI
        changeSort = False
        if event == "Song":
            libSort = "title"
            changeSort = True
        if event == "Length":
            libSort = "runtimeseconds"
            changeSort = True
        if event == "Genre":
            libSort = "genres"
            changeSort = True
        if event == "Artist":
            libSort = "artistname"
            changeSort = True
        if event == "Album":
            libSort = "albumname"
            changeSort = True
        if event == "Year":
            libSort = "releaseyear"
            changeSort = True
        if event == "Rating":
            libSort = "avgrating"
            changeSort = True

        if event == "Song0":
            favSort = "title"
            changeSort = True
        if event == "Length1":
            favSort = "runtimeseconds"
            changeSort = True
        if event == "Genre2":
            favSort = "genres"
            changeSort = True
        if event == "Artist3":
            favSort = "artistname"
            changeSort = True
        if event == "Album4":
            favSort = "albumname"
            changeSort = True
        if event == "Year5":
            favSort = "releaseyear"
            changeSort = True
        if event == "Rating6":
            favSort = "avgrating"
            changeSort = True
        if event == "Rate Song":
            rate_window = create_rate_window()
            event, values = rate_window.read()
            print(values[0],  values[1])
            if int(values[1]) > 5 or int(values[1]) < 0:
                sg.Popup("Invalid Rate Value")
            else:

                rate_song(values[0],values[1])
                rate_window.close()

        #execute the sql statements to get title, songid, userid, and username from respective table
        cur.execute("SELECT title, songid FROM song")
        song = cur.fetchall()
        cur.execute("SELECT userid, username FROM users")
        all_userid = cur.fetchall()
        cur.execute("SELECT songid FROM favorites")
        favorites = cur.fetchall()
        no_listID = False
        found = False
        duplicate = False

        #if remove button is pressed, it calls the remove_from_favorites function which removes a song name the user enters in 
        # from their own favorites list
        if event == "Remove ":
            #print(values[2])
            
            user_id = ""
            for i in all_userid:
                if i[1] == user:
                     user_id= i[0]
                     
            
            operation = remove_from_favorites(values[2], user_id)
            #print("we just called the function to remove the song with a specifci user_id")
            """
            if operation == True:
                sg.Popup("Removal of song is sucessful!")
            elif operation == False:
                sg.Popup("Error! Removal could not be done because the song does not exist as the user favorite's!")
            """
        # we know whether we have removed the song based off the operation return value
        if operation == True and event == "Remove":
            sg.Popup("Removal of song is sucessful!")
        if operation == False and event == "Remove":
            sg.Popup("Error! Removal could not be done because the song does not exist as the user favorite's!")
        #when submit button is pressed look for the name of the song the user put in textbox
        #if it is found it will set bool to true which will trigger the next if statement
        if event == "Submit":
            
            for i in song:
                if i[0] == values[0]:
                    found = True
                    songFound = i[1]
                    #sg.Popup(i[0])
      
        #if the song is in the database find the userid of the user thats currently signed in 
        #once user is found insert the song that was chosen into the favorites table
        if found == True:
            
             #search for userid that matches current signed on user
             for i in all_userid:
                 if i[1] == user:
                     userID= i[0]
                     #print("found user", i[0])

             #duplicate check for song re entries
             cur.execute("SELECT title FROM song, favorites WHERE song.songid = favorites.songid AND userid = %s",(userID,))
             duplicate_check = cur.fetchall()
             
             #select the listid that corresponds to the current user signed on 
             cur.execute("SELECT DISTINCT listid FROM favorites WHERE userid = %s",(userID,))
             listID = cur.fetchall()
             
             #if current user does not have a favorites list then create a listid that corresponds to users music list
             if not listID:
                 no_listID = True
                 random_num = random.randint(100,999)
             else:
                 listID = [i[0] for i in listID]
                 x = listID[0]
                 
                 
            #check if song exists in the favorites 
             
            
             for i in duplicate_check:
                  if i[0] == values[0]:
                      found = False
                      duplicate = True
                      sg.Popup("Song already in Favorites!")
             #if user does not exists give new listid 
             if no_listID == True:
                 insert_song_toFavorites = "INSERT INTO Favorites (songid ,userid, listid) VALUES (%s,%s,%s)"
                 song = [(songFound, userID, random_num)]
                 cur.executemany(insert_song_toFavorites,song)
                 sg.Popup("Song Successfully Added!\n")
                 con.commit()
             #if user exists insert into respective favorites list
             if duplicate == False and no_listID == False:
                 insert_song_toFavorites = "INSERT INTO Favorites (songid ,userid, listid) VALUES (%s,%s,%s)"
                 song = [(songFound, userID, x)]
                 cur.executemany(insert_song_toFavorites,song)
                 sg.Popup("Song Successfully Added!\n")
                 con.commit()

        
        if found == False and event == "Submit":
            sg.Popup("Failed to Add to List!\n") 

        """
        if operation == True:
            sg.Popup("Removal of song is sucessful!")
        elif operation == False:
            sg.Popup("Error! Removal could not be done because the song does not exist as the user favorite's!")
            """


        #display current list of songs in a popup 
        """if found == True:
            sg.Popup("Current list")
            cur.execute("SELECT title FROM song, favorites WHERE song.songid = favorites.songid AND userid = %s", (userID,))
            song_list = cur.fetchall()
            sg.Popup(song_list)
        else:
            sg.Popup("Failed to add to Favorites")
          """  
        #moved to beginning, could be placed at beginning or end
        #if event == sg.WIN_CLOSED:
        #        cur.close()
        #        con.close()
        #        sys.exit()



"""
    while sign_on == 0:
         
         login_window = create_login_window()
         
         event, values = login_window.read()
         #might have to open the libary inside the login window otherwise its gonna ask for
         #pass and username twice
         sign_on = login(values[0], values[1], login_window, event)
         print("current sign value", sign_on)
         if sign_on == 1:
             login_window.close()
             
             library_window = create_library_UI()
             event, values = library_window.read()
         elif sign_on == 2:
             login_window.close()
             create_account()
         elif event == "Create Account":
             login_window.close()
             create_account()
         elif event == sg.WIN_CLOSED:
             cur.close()
             con.close()
             sys.exit()
   """    
        

main()