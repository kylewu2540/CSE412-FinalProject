#!/usr/bin/env python3
"""
Created on Mon Mar 14 13:51:45 2022

Written by Jake Kenny
"""

import PySimpleGUI as sg
import sys
import psycopg2 as pg
"""connect to pg4admin database  """
con = pg.connect(host="localhost", user="postgres", password="412group", dbname="musicDB")

cur = con.cursor()
"""creates the tables with attributes and constraints  """
create_song = '''CREATE TABLE IF NOT EXISTS song (
                    songID  int PRIMARY KEY,
                    name    varchar(40) NOT NULL,
                    Title   varchar(40) NOT NULL,
                    ArtistID    int,
                    runTimeSeconds  int, 
                    genres  varchar(20), 
                    artistName  varchar(20) NOT NULL 

                    )'''
create_users = ''' CREATE TABLE IF NOT EXISTS Users (
                    UserID  int PRIMARY KEY,
                    fname   varchar(20) NOT NULL, 
                    lname   varchar(20) NOT NULL, 
                    emailAddr varchar(40) NOT NULL, 
                    userPass    varchar(50) NOT NULL


                    )'''
create_artist = ''' CREATE TABLE IF NOT EXISTS Artist (
                    ArtistID  int PRIMARY KEY,
                    fname   varchar(20) NOT NULL, 
                    lname   varchar(20) NOT NULL
                    
                    )'''

create_album = ''' CREATE TABLE IF NOT EXISTS Album (
                    AlbumID  int PRIMARY KEY,
                    albumName   varchar(40) NOT NULL, 
                    artistName   varchar(20) NOT NULL, 
                    releaseYear     int, 
                    genres      varchar(20)
                    
                    )'''
create_rating = '''CREATE TABLE IF NOT EXISTS rating (
                    avgRating   int,
                    songID      int PRIMARY KEY
                    )'''

create_favorites = ''' CREATE TABLE IF NOT EXISTS favorites (
                    userID  int,
                    listID  int PRIMARY KEY
                   )'''

"""executes the sql commands for creating the tables  """
cur.execute(create_song)
cur.execute(create_users)
cur.execute(create_artist)
cur.execute(create_album)
cur.execute(create_rating)
cur.execute(create_favorites)
        
""" commits them so they show up on database"""
con.commit()
""" close connections""" 
cur.close()
con.close()

#Temp login dictionary. Will be replaced with a SQL database
accounts = {'Admin':'123456'}

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
       [sg.Text("Password: "), sg.InputText(password_char = '*')],
       [sg.Button("Create Account")]
       ] 
    create_account_window = sg.Window("CSE 412 Project", create_account_layout, margins = (100, 50))
    return create_account_window
  
#The music library UI is composed of the library and favorites tab
#These two tabs are very similar; the only difference is that the table in favorites is a subset of the table in library
def create_library_UI():
    """
    TODO:
        1. Format the tables to fit the screen
        2. Set the 'values' parameter equal to the SQL database
    """
    library_layout = [
        [sg.Table(values = [['0', '0']], headings = ['0', '1'])]
        ]
    favorites_layout = [
        [sg.Table(values = [['0', '0']], headings = ['0', '1'])]
        ]
    tabgrp = [
        [sg.TabGroup([
            [sg.Tab('Library', library_layout, key = '-LIBRARY_TAB-')],
            [sg.Tab('Favorites', favorites_layout, key = '-FAVORITES_TAB-')]
            ], key = '-TABGRP-')]
        ] 
    library_UI_window = sg.Window("CSE 412 Project", tabgrp).finalize()
    library_UI_window.maximize()
    library_UI_window['-TABGRP-'].expand(True, True)
    return library_UI_window

#Returns 0 on an unsuccessful login, 1 on a successful login, and 2 if the user wants to create an account
#Parameters: the provided username, the provided password, the login window, the login window's event handler
#I made the event handler a parameter to avoid creating multiple event handlers for the same window
def login(username, password, login_window, event):
    if username in accounts and password == accounts.get(username):
        login_window.close()
        return 1
    elif event == "Create Account":
        login_window.close()
        return 2
    elif event == sg.WIN_CLOSED:
        sys.exit()
    else:
        login_window.close()
        incorrect_login_window = create_incorrect_login_window()
        event, values = incorrect_login_window.read()
        if event == "OK" or event == sg.WIN_CLOSED:
            incorrect_login_window.close()
        return 0
            
#Inserts the username and password as a key-vakue pair in accounts
#This should eventually interact with an SQL database, not a Python dictionary            
def create_account():
    create_account_window = create_create_account_window()
    event, values = create_account_window.read()
    if event == "Create Account":
        #TODO: Replace the following line of code with an SQL command to add the username and password to the database
        accounts[values[0]] = values[1]
        create_account_window.close()
    main()

def main():
    login_window = create_login_window()
    event, values = login_window.read()
    if event == "Log In":
        #Replace this if statement with an SQL command that performs the same task
        sign_on = login(values[0], values[1], login_window, event)
        #The user is continually displayed an error message and prompted to log in as long as they keep entering
        #incorrect usernames and passwords
        while sign_on == 0:
            login_window = create_login_window()
            event, values = login_window.read()
            sign_on = login(values[0], values[1], login_window, event)
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
        sys.exit()
        
main()
        
        
