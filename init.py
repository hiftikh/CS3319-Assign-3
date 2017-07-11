from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

###################### HOME ######################

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/staff/')
def staff():
	return render_template('staff/index.html')

@app.route('/customer/')
def customer():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()

	query = ("SELECT MovieName,idShowing,ShowingDateTime FROM Showing, Movie WHERE Movie_idMovie=idMovie ORDER BY ShowingDateTime")
	cursor.execute(query)
	movies=cursor.fetchall()

	query = ("SELECT FirstName FROM Customer")
	cursor.execute(query)
	userdata=cursor.fetchall()

	query = ("SELECT MovieName FROM Movie")
	cursor.execute(query)
	moviename=cursor.fetchall()

	query = ("SELECT DISTINCT ShowingDateTime FROM Showing ORDER BY ShowingDateTime")
	cursor.execute(query)
	datetime=cursor.fetchall()

	query = ("SELECT DISTINCT Genre FROM Genre")
	cursor.execute(query)
	genre=cursor.fetchall()

	cnx.commit()
	cnx.close()
	return render_template('customer/index.html', genre=genre, userdata=userdata, moviename=moviename, datetime=datetime)

###################### CUSTOMER ######################

@app.route('/customer/customerProfile.html')
def customerProfile():
	return render_template('customer/customerProfile.html')

@app.route('/customerProfileButton', methods=['POST'])
def customerProfileButton():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	idCustomer=request.form['userdata']
	query = ("SELECT * FROM Customer WHERE FirstName=%s")
	cursor.execute(query,(idCustomer,))
	userdata=cursor.fetchall()
	query = ("SELECT MovieName, Rating FROM Attend, Movie, Showing, Customer WHERE FirstName=%s and Showing_idShowing=idShowing and Movie_idMovie=idMovie")
	cursor.execute(query,(idCustomer,))
	movieattend=cursor.fetchall()
	cnx.close()
	return render_template('customer/customerProfile.html', userdata=userdata, movieattend=movieattend)

@app.route('/buyTicketButton', methods=['POST'])
def buyTicketButton():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	data=[request.form['moviename'], request.form['userdata']]
	query="INSERT INTO Attend (Customer_idCustomer,Showing_idShowing) VALUES(%s,%s)"
	cursor.execute(query, data)
	cnx.commit()
	cnx.close()
	return render_template('customer/index.html')

@app.route('/rateMovieButton', methods=['POST'])
def rateMovieButton():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	data=[request.form['rating'], request.form['userdata'], request.form['moviename']]
	query = ("UPDATE Attend SET Rating=%s WHERE Customer_idCustomer=%s and Showing_idShowing= %s") 
	cursor.execute(query,data)
	cnx.commit()
	cnx.close()
	return render_template('customer/index.html')

@app.route('/customer/search.html')
def search():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	query = ("SELECT DISTINCT Genre FROM Genre")
	cursor.execute(query)
	genre=cursor.fetchall()
	query =("SELECT DISTINCT ShowingDateTime FROM Showing ORDER BY ShowingDateTime")
	cursor.execute(query)
	Date=cursor.fetchall()
	cnx.commit()
	cnx.close()
	return render_template('customer/search.html', genre=genre, Date=Date)

@app.route('/searchButton', methods=['POST'])
def searchButton():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	data= [request.form['moviename'], request.form['seat'], request.form['startdate'], request.form['enddate'], request.form['genre']]
	if (data[0] != None and data[0] != ""):
		query=("SELECT MovieName, ShowingDateTime, TheatreRoom_RoomNumber, TicketPrice, Capacity-count(Customer_idCustomer) FROM Movie, TheatreRoom, Showing, Attend WHERE MovieName='"+moviename+ "' and ShowingDateTime > '"+startdate+"'and ShowingDateTime < '"+enddate+"'  and Movie.idMovie = Showing.Movie_idMovie and TheatreRoom_RoomNumber=RoomNumber and Showing_idShowing = idShowing ORDER BY ShowingDateTime")
		cursor.execute(query)
		search=cursor.fetchall()
	else:
		query=("SELECT MovieName, RoomNumber, ShowingDateTime, TicketPrice FROM Movie, Genre, TheatreRoom, Showing WHERE Movie.idMovie = Genre.Movie_idMovie and Showing.TheatreRoom_RoomNumber = TheatreRoom.RoomNumber and Showing.Movie_idMovie=Movie.idMovie and Genre = '"+genre+"' ORDER BY ShowingDateTime")
		cursor.execute(query)
		search=cursor.fetchall()

	cnx.commit()
	cnx.close()
	return render_template('customer/search.html', search=search)

###################### MOVIE ######################

@app.route('/staff/addMovie.html')
def addMovie():
	return render_template('staff/addMovie.html')

@app.route('/addMovieButton', methods=['POST'])
def addMovieButton():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	data = [request.form['idMovie'], request.form['MovieName'], request.form['MovieYear']]
	query = "INSERT INTO Movie (idMovie, MovieName, MovieYear) VALUES(%s, %s, %s)"
	cursor.execute(query, data)
	cnx.commit()
	cnx.close()
	return render_template("staff/index.html")

@app.route('/staff/deleteMovie.html')
def deleteMovie():
    return render_template('staff/deleteMovie.html')

@app.route('/deleteMovieButton', methods=['POST'])
def deleteMovieButton():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	data = request.form['idMovie']
	query = "DELETE FROM Genre WHERE Movie_idMovie=%s"
	cursor.execute(query, (data,))
	query = "DELETE FROM Showing WHERE Movie_idMovie=%s"
	cursor.execute(query, (data,))
	query = "DELETE FROM Movie WHERE idMovie=%s"
	cursor.execute(query, (data,))
	cnx.commit()
	cnx.close()
	return render_template("staff/index.html")

@app.route('/staff/modifyMovie.html')
def modifyMovie():
    return render_template('staff/modifyMovie.html')

@app.route('/modifyMovieButton', methods=['POST'])
def modifyMovieButton():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	data=(request.form['idMovie'], request.form['MovieName'], request.form['MovieYear'])
	if (data[1] != "" and data[1] != None):
		tdata=(request.form['MovieName'], request.form['idMovie'])
		query = "UPDATE Movie SET MovieName=%s WHERE idMovie=%s"
		cursor.execute(query, tdata)
		cnx.commit()
	if (data[2] != "" and data[2] != None):
		tdata=(request.form['MovieYear'], request.form['idMovie'])
		query = "UPDATE Movie SET MovieYear=%s WHERE idMovie=%s"
		cursor.execute(query, tdata)
		cnx.commit()
	cnx.close()
	return render_template("staff/index.html")

@app.route('/staff/listMovie.html')
def listMovie():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	query = ("SELECT * from Movie")
	cursor.execute(query)
	movies=cursor.fetchall()
	cnx.close()
	return render_template('staff/listMovie.html', Movie=movies)

###################### GENRE ######################

@app.route('/staff/addGenre.html')
def addGenre():
	return render_template('staff/addGenre.html')

@app.route('/addGenreButton', methods=['POST'])
def addGenreButton():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	data=(request.form['Genre'], request.form['idMovie'])
	if (data[1] != "" and data[1] != None):
		query = "INSERT INTO Genre (Genre, Movie_idMovie) VALUES(%s, %s)"
		cursor.execute(query, data)
		cnx.commit()
	cnx.close()
	return render_template("staff/index.html")

@app.route('/staff/deleteGenre.html')
def deleteGenre():
    return render_template('staff/deleteGenre.html')

@app.route('/deleteGenreButton', methods=['POST'])
def deleteButtonGenre():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	data = request.form['idMovie']
	if (data[0]!= "" and data[0]!= None):
		query = "DELETE FROM Genre WHERE Movie_idMovie=%s"
		cursor.execute(query, (data,))
		cnx.commit()
	cnx.close()
	return render_template('staff/index.html')

@app.route('/staff/listGenre.html')
def listGenre():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	query = ("SELECT * from Genre")
	cursor.execute(query)
	genres=cursor.fetchall()
	cnx.close()
	return render_template('staff/listGenre.html', Genre=genres)

###################### ROOM ######################

@app.route('/staff/addRoom.html')
def addRoom():
    return render_template('staff/addRoom.html')

@app.route('/addRoomButton', methods=['POST'])
def addRoomButton():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	data=(request.form['RoomNumber'], request.form['Capacity'])
	query = "INSERT INTO TheatreRoom(RoomNumber, Capacity) VALUES(%s, %s)"
	cursor.execute(query, data)
	cnx.commit()
	cnx.close()
	return render_template("staff/index.html")

@app.route('/staff/deleteRoom.html')
def deleteRoom():
	return render_template('staff/deleteRoom.html')

@app.route('/deleteRoomButton', methods=['POST'])
def deleteRoomButton():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	data=(request.form['RoomNumber'])
	query = "DELETE FROM TheatreRoom WHERE RoomNumber=%s;"
	cursor.execute(query, (data,))
	cnx.commit()
	return render_template('staff/index.html')

@app.route('/staff/modifyRoom.html')
def modifyRoom():
	return render_template('staff/modifyRoom.html')

@app.route('/modifyRoomButton', methods=['POST'])
def modifyRoomButton():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	data=(request.form['RoomNumber'], request.form['Capacity'])
	query = "UPDATE TheatreRoom Set Capacity=%s WHERE RoomNumber=%s"
	cursor.execute(query, data)
	cnx.commit()
	return render_template('staff/index.html')

@app.route('/staff/listRoom.html')
def listRoom():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	query = ("SELECT * from TheatreRoom")
	cursor.execute(query)
	rooms=cursor.fetchall()
	cnx.close()
	return render_template('staff/listRoom.html', Room=rooms)

###################### SHOWING ######################

@app.route('/staff/addShowing.html')
def addShowing():
    return render_template('staff/addShowing.html')

@app.route('/addShowingButton', methods=['POST'])
def addShowingButton():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	data=(request.form['idShowing'], request.form['ShowingDateTime'], request.form['Movie_idMovie'], request.form['TheatreRoom_RoomNumber'], request.form['TicketPrice'])
	query = "INSERT INTO Showing(idShowing, ShowingDateTime, Movie_idMovie, TheatreRoom_RoomNumber, TicketPrice) VALUES(%s, %s, %s, %s, %s)"
	cursor.execute(query, data)
	cnx.commit()
	cnx.close()
	return render_template("staff/index.html")

@app.route('/staff/deleteShowing.html')
def deleteShowing():
    return render_template('staff/deleteShowing.html')

@app.route('/deleteShowingButton', methods=['POST'])
def deleteShowingButton():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	data=(request.form['idShowing'], request.form['Movie_idMovie'], request.form['TheatreRoom_RoomNumber'])
	query = "DELETE FROM Showing WHERE idShowing=%s and Movie_idMovie=%s and TheatreRoom_RoomNumber=%s;"
	cursor.execute(query, (data))
	cnx.commit()
	return render_template('staff/index.html')

@app.route('/staff/modifyShowing.html')
def modifyShowing():
    return render_template('staff/modifyShowing.html')

@app.route('/modifyShowingButton', methods=['POST'])
def modifyShowingButton():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	data=(request.form['idShowing'], request.form['ShowingDateTime'], request.form['Movie_idMovie'], request.form['TheatreRoom_RoomNumber'], request.form['TicketPrice'])
	if (data[0] != None and data[0] != "" and data[2] != None and data[2] != "" and data[3] != "" and data[3] != None):
		if (data[1] != "" and data[1] != None):
			tData = (request.form['ShowingDateTime'], request.form['idShowing'], request.form['Movie_idMovie'], request.form['TheatreRoom_RoomNumber'])
			query = "UPDATE Showing Set ShowingDateTime=%s WHERE idShowing=%s and Movie_idMovie=%s and TheatreRoom_RoomNumber=%s"
			cursor.execute(query, tData)
			cnx.commit()
		if (data[4] != None and data[4] != ""):
			tData = (request.form['TicketPrice'], request.form['idShowing'], request.form['Movie_idMovie'], request.form['TheatreRoom_RoomNumber'])
			query = "UPDATE Showing Set TicketPrice=%s WHERE idShowing=%s and Movie_idMovie=%s and TheatreRoom_RoomNumber=%s"
			cursor.execute(query, tData)
			cnx.commit()
	return render_template('staff/index.html')

@app.route('/staff/listShowing.html')
def listShowing():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	query = ("SELECT * from Showing")
	cursor.execute(query)
	showings=cursor.fetchall()
	cnx.close()
	return render_template('staff/listShowing.html', Showing=showings)

###################### CUSTOMER ######################

@app.route('/staff/addCustomer.html')
def addCustomer():
    return render_template('staff/addCustomer.html')

@app.route('/addCustomerButton', methods=['POST'])
def addCustomerButton():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	data=(request.form['idCustomer'], request.form['FirstName'], request.form['LastName'], request.form['EmailAddress'], request.form['Sex'])
	if (data[0] != "" and data[0] != None):
		query = "INSERT INTO Customer(idCustomer, FirstName, LastName, EmailAddress, Sex) VALUES(%s, %s, %s, %s, %s);"
		cursor.execute(query, data)
		cnx.commit()
	cnx.close()
	return render_template("staff/index.html")

@app.route('/staff/deleteCustomer.html')
def deleteCustomer():
    return render_template('staff/deleteCustomer.html')

@app.route('/deleteCustomerButton', methods=['POST'])
def deleteCustomerButton():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	data=(request.form['idCustomer'])
	if (data[0] !="" and data[0] != None):
		query = "DELETE FROM Customer WHERE idCustomer=%s;"
		cursor.execute(query, (data,))
		cnx.commit()
	return render_template("staff/index.html")

@app.route('/staff/modifyCustomer.html')
def modifyCustomer():
    return render_template('staff/modifyCustomer.html')

@app.route('/modifyCustomerButton', methods=['POST'])
def modifyCustomerButton():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	data=(request.form['idCustomer'], request.form['FirstName'], request.form['LastName'], request.form['EmailAddress'], request.form['Sex'])
	if (data[0] != "" and data[0] != None):
		if (data[1] != "" and data[1] != None):
			tdata = (request.form['FirstName'], request.form['idCustomer'])
			query = "UPDATE Customer Set FirstName=%s WHERE idCustomer=%s;"
			cursor.execute(query, tdata)
			cnx.commit()
		if (data[2] != None and data[2] != ""):
			tdata = (request.form['LastName'], request.form['idCustomer'])
			query = "UPDATE Customer Set LastName=%s WHERE idCustomer=%s;"
			cursor.execute(query, tdata)
			cnx.commit()
		if (data[3] != None and data[3] != ""):
			tdata = (request.form['EmailAddress'], request.form['idCustomer'])
			query = "UPDATE Customer Set EmailAddress=%s WHERE idCustomer=%s;"
			cursor.execute(query, tdata)
			cnx.commit()
		if (data[4] != None and data[4] != ""):
			tdata = (request.form['Sex'], request.form['idCustomer'])
			query = "UPDATE Customer Set Sex=%s WHERE idCustomer=%s;"
			cursor.execute(query, tdata)
			cnx.commit()
	cnx.close()
	return render_template("staff/index.html")

@app.route('/staff/listCustomer.html')
def listCustomer():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	query = ("SELECT * from Customer")
	cursor.execute(query)
	customers=cursor.fetchall()
	cnx.close()
	return render_template('staff/listCustomer.html', Customer=customers)

###################### ATTEND ######################

@app.route('/staff/listAttendee.html')
def listAttendee():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	query = ("SELECT * from Attend")
	cursor.execute(query)
	attends=cursor.fetchall()
	cnx.close()
	return render_template('staff/listAttendee.html', Attend=attends)

###################### MAIN ######################

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)