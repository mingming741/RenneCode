import java.sql.*;
import java.util.Scanner; 
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.Date;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.InputMismatchException;

public class Main {
	public static Scanner reader;
	public static Connection connection;
	public static ResultSet result;
	public static Statement stmt, stmt2;
	
	public static void main(String[] args) throws Exception {
		init();
		op_menu();
	}
	
	public static void init() {
		reader = new Scanner(System.in); 
		connection = null;
		result = null;
		dbConnection();
	}
	
	public static void exit() {
		reader.close();
		System.exit(0);
	}
	
	public static void dbConnection() {	
		try{	
			Class.forName("com.mysql.jdbc.Driver").newInstance();
			connection = DriverManager.getConnection("jdbc:mysql://appsrvdb.cse.cuhk.edu.hk:3306/CSCI3170S41","CSCI3170S41","987654321"); 
			stmt = connection.createStatement();
			stmt2 = connection.createStatement();
		}
		catch(Exception e){
			e.printStackTrace();
		}
	}
	
	public static void op_menu() {
		while(true) {
			System.out.print("--Main menu--\n"
					+ "What kinds of operation would you like to perform\n"
					+ "1. Operations for administrator\n"
					+ "2. Operations for library user\n"
					+ "3. Operations for librarian\n"
					+ "4. Exit this program\n"
					+ "Enter your Choice: ");
			int operation = reader.nextInt();
			if(operation == 1) {
				op_admin();
			}else if(operation == 2) {
				op_user();
			}else if(operation == 3) {
				op_librarian();
			}else if(operation == 4) {
				exit();
			}
			else {
				System.out.println("[Error]: Wrong operation, please input right opeartion\n");
			}
			System.out.println("");
		}
	}
	
	public static void op_admin() {
		System.out.print("--Operations for administrator menu--\n"
				+ "What kinds of operation would you like to perform\n"
				+ "1. Create All table\n"
				+ "2. Delete All table\n"
				+ "3. Load Data\n"
				+ "4. Show number of record in each table\n"
				+ "5. Return to the main meun\n"
				+ "Enter your Choice: ");
		int operation = reader.nextInt();
		if(operation == 1) {
			db_createAllTable();
		}else if(operation == 2) {
			db_deleteAllTable();
		}else if(operation == 3) {
			db_loadData();
		}else if(operation == 4) {
			db_showNumberReocd();
		}
		else if(operation == 5) {
			op_menu();
		}
		else {
			System.out.println("[Error]: Wrong operation, please input right opeartion\n");
			op_admin();
		}
	}
	
	public static void op_user() {
		System.out.print("--Operations for library user menu--\n"
				+ "What kinds of operation would you like to perform\n"
				+ "1. Search for Books\n"
				+ "2. Show checkout records of a user\n"
				+ "3. Return to the main meun\n"
				+ "Enter your Choice: ");
		int operation = reader.nextInt();
		if(operation == 1) {
			db_searchForBooks();
		}else if(operation == 2) {
			db_showCheckoutRecord();
		}else if(operation == 3) {
			op_menu();
		}
		else {
			System.out.println("[Error]: Wrong operation, please input right opeartion\n");
			op_user();
		}
	}
	
	public static void op_librarian() {
		System.out.print("--Operations for librarian menu--\n"
				+ "What kinds of operation would you like to perform\n"
				+ "1. Book Borrowing\n"
				+ "2. Book Returning\n"
				+ "3. List all un-returned book copies which are checked-out within a period\n"
				+ "4. Return to the main meun\n"
				+ "Enter your Choice: ");
		int operation = reader.nextInt();
		if(operation == 1) {
			db_bookBorrowing();
		}else if(operation == 2) {
			db_bookreturning();
		}else if(operation == 3) {
			db_listUnreturnedBook();
		}else if(operation == 4) {
			op_menu();
		}
		else {
			System.out.println("[Error]: Wrong operation, please input right opeartion\n");
			op_user();
		}
	}
	
	public static void db_createAllTable() {
		System.out.println("Admin: Create All Table");
		try {
			stmt.execute("CREATE TABLE category(\r\n" + 
					"  id Integer PRIMARY KEY,\r\n" + 
					"  loan_period Integer,\r\n" + 
					"  max_books Integer,\r\n" + 
					"  CHECK (id>=1 AND id<=9),\r\n" + 
					"  CHECK (loan_period>=1 AND loan_period<=99),\r\n" + 
					"  CHECK (max_books>=1 AND max_books<=99)\r\n" + 
					");");
			stmt.execute("CREATE TABLE user(\r\n" + 
					"  id char(10) PRIMARY KEY,\r\n" + 
					"  name varchar(25),\r\n" + 
					"  address varchar(100),\r\n" + 
					"  category_id Integer,\r\n" + 
					"  CHECK(category_id>=1 AND category_id<=9),\r\n" + 
					"  FOREIGN KEY (category_id) REFERENCES category(id)\r\n" + 
					");");
			stmt.execute("CREATE TABLE book(\r\n" + 
					"  call_number char(8) PRIMARY KEY,\r\n" + 
					"  title varchar(30) NOT NULL,\r\n" + 
					"  publish_date DATE,\r\n" + 
					"  CHECK(title <> '')\r\n" + 
					");");
			stmt.execute("CREATE TABLE copy(\r\n" + 
					"  call_number char(8),\r\n" + 
					"  copy_number Integer,\r\n" + 
					"  CHECK(copy_number >= 1 AND copy_number <= 9),\r\n" + 
					"  PRIMARY KEY(call_number, copy_number),\r\n" + 
					"  FOREIGN KEY (call_number) REFERENCES book(call_number)\r\n" + 
					");");
			stmt.execute("CREATE TABLE checkout_record(\r\n" + 
					"  user_id char(10),\r\n" + 
					"  call_number char(8) NOT NULL,\r\n" + 
					"  copy_number Integer,\r\n" + 
					"  checkout_date DATE,\r\n" + 
					"  return_date DATE,\r\n" + 
					"  PRIMARY KEY(user_id, call_number, copy_number, checkout_date),\r\n" + 
					"  CHECK(copy_number >=1 AND copy_number <=9),\r\n" + 
					"  FOREIGN KEY (user_id) REFERENCES user(id),\r\n" + 
					"  FOREIGN KEY (call_number,copy_number) REFERENCES copy(call_number,copy_number)\r\n" + 
					");");
			stmt.execute("CREATE TABLE author(\r\n" + 
					"  name varchar(25),\r\n" + 
					"  call_number char(8),\r\n" + 
					"  PRIMARY KEY(name, call_number),\r\n" + 
					"  FOREIGN KEY (call_number) REFERENCES book(call_number)\r\n" + 
					");");
		}
		catch(Exception e){
			System.out.println("[Error]: SQL Query Error");
		}
		System.out.println("[OK]: Processing...Done! Database is initialized");
	}
	
	public static void db_deleteAllTable() {
		System.out.println("Admin: Delete All Table");
		try {
			stmt.execute("DROP TABLE IF EXISTS checkout_record");
			stmt.execute("DROP TABLE IF EXISTS copy;");		
			stmt.execute("DROP TABLE IF EXISTS user;");
			stmt.execute("DROP TABLE IF EXISTS book;");		
			stmt.execute("DROP TABLE IF EXISTS author;");
			stmt.execute("DROP TABLE IF EXISTS category;");
		}
		catch(Exception e){
			System.out.println("[Error]: SQL Query Error");
		}
		System.out.println("[OK]: Processing...Done! Database is removed");
	}
	
	public static void db_loadData() {
		reader.nextLine();
		System.out.println("Admin: Load Data");
	    System.out.print("Type the source Data Folder Path: ");
	    String path = reader.nextLine();
	    String line;
	    String query;
	    BufferedReader br;
	    try {
	    	br = new BufferedReader(new FileReader(path + "/book.txt"));
	    	while((line = br.readLine()) != null) {
	    		String[] parts = line.split("	");
	    		String date = parts[4];
	    		String[] datesplit  = date.split("/");
	    		parts[4] = datesplit[2] + "/" + datesplit[1] + "/" + datesplit[0];		
	    		query = "Insert into book values ( '" + parts[0] + "','" + parts[2] + "','" + parts[4] + "');";	
	    		//System.out.println(query);
				stmt.executeUpdate(query);
	    		String[] authorsplit = parts[3].split(",");
	    		for(int i = 0;i < authorsplit.length; i++) {
	    			query = "Insert into author values ( '" + authorsplit[i] + "','" + parts[0] + "');";
	    			//System.out.println(query);
	    			stmt.executeUpdate(query);
	    		}
	    		for(int i = 0;i < Integer.parseInt(parts[1]); i++) {
	    			query = "Insert into copy values ( '" + parts[0] + "','" + (i + 1) + "');";
	    			//System.out.println(query);
	    			stmt.executeUpdate(query);
	    		}
	    	}
	    	br = new BufferedReader(new FileReader(path + "/category.txt"));
	    	while ((line = br.readLine()) != null) {
	    		String[] parts = line.split("	");
	    		query = "Insert into category values ( " + parts[0] + "," + parts[1] + "," + parts[2] + ");";	
	    		//System.out.println(query);
				stmt.executeUpdate(query);
	    	}
	    	br = new BufferedReader(new FileReader(path + "/user.txt"));
	    	while ((line = br.readLine()) != null) {
	    		String[] parts = line.split("	");
	    		query = "Insert into user values ( '" + parts[0] + "','" + parts[1] + "',\"" + parts[2] + "\"," + parts[3] + ");";	
	    		//System.out.println(query);
				stmt.executeUpdate(query);
	    	}
	    	br = new BufferedReader(new FileReader(path + "/checkout.txt"));
	    	while ((line = br.readLine()) != null) {
	    		String[] parts = line.split("	");
	    		String date = parts[3];
	    		String[] datesplit  = date.split("/");
	    		parts[3] = datesplit[2] + "/" + datesplit[1] + "/" + datesplit[0];	
	    		if(!parts[4].equals("null")) {
	    			//System.out.println(parts[4]);
	    			String date2 = parts[4];
		    		String [] datesplit2  = date2.split("/");
		    		parts[4] = "'" + datesplit2[2] + "/" + datesplit2[1] + "/" + datesplit2[0] + "'";
	    		}
	    		query = "Insert into checkout_record values ( '" + parts[2] + "','" + parts[0] + "'," + parts[1] + ",'" + parts[3] + "'," + parts[4] + ");";	
	    		//System.out.println(query);
				stmt.executeUpdate(query);
	    	}
	    } catch (IOException e) {
	    	System.err.println("[Error]: IO Error!");
	    } catch (SQLException e) {
			System.out.println("[Error]: SQL Query Error");
		}
	    System.out.println("[OK]: Processing...Done! Data are successfully loaded");
	}
	
	public static void db_showNumberReocd() {
		System.out.println("Admin: Show Number Record in each Table");
		String query;
		try {
			query = "Select Count(*) From category";
			result = stmt.executeQuery(query);
			while(result.next()){
				System.out.println("category: " + result.getString("Count(*)"));
			}
			query = "Select Count(*) From user";
			result = stmt.executeQuery(query);
			while(result.next()){
				System.out.println("user: " + result.getString("Count(*)"));
			}
			query = "Select Count(*) From book";
			result = stmt.executeQuery(query);
			while(result.next()){
				System.out.println("book: " + result.getString("Count(*)"));
			}
			query = "Select Count(*) From copy";
			result = stmt.executeQuery(query);
			while(result.next()){
				System.out.println("copy: " + result.getString("Count(*)"));
			}
			query = "Select Count(*) From checkout_record";
			result = stmt.executeQuery(query);
			while(result.next()){
				System.out.println("checkout_record: " + result.getString("Count(*)"));
			}
			query = "Select Count(*) From author";
			result = stmt.executeQuery(query);
			while(result.next()){
				System.out.println("author: " + result.getString("Count(*)"));
			}
		}
		catch(Exception e){
			System.out.println("[Error]: SQL Query Error");
		}
	}
	
	public static void db_searchForBooks() {
		System.out.println("User: Search For Books");
		System.out.print("Choose the Search criterion\n"
				+ "1. call number\n"
				+ "2. title\n"
				+ "3. author\n"
				+ "Enter the search criterion: ");
		int operation = reader.nextInt();
		String key = "";
		String attribute = "";
		String where = "";
		if(operation == 1) {
			reader.nextLine();
			System.out.print("Type your call number: ");
			key = reader.nextLine();
			attribute = "call_number";	
			where = "where " + attribute + " = '" + key + "' order by call_number";
		}else if(operation == 2) {
			reader.nextLine();
			System.out.print("Type your title: ");
			key = reader.nextLine();
			attribute = "title";
			where = "where " + attribute + " like binary '%" + key + "%' order by call_number";
		}else if(operation == 3) {
			reader.nextLine();
			System.out.print("Type author: ");
			key = reader.nextLine();
			where = "where call_number in (\r\n" + 
					"  Select call_number\r\n" + 
					"  from author\r\n" + 
					"  where name like binary '%" + key + "%'\r\n" + 
					") order by call_number";
		}
		else {
			System.out.println("[Error]: Wrong operation, please input right opeartion\n");
			db_searchForBooks();
		}
		System.out.println("| Call Number | Title | Author | Available No. of Copies |");
		String query = "Select * From("
				+ "Select t.call_number, title, (number - borrow) as available\r\n" + 
				"from(\r\n" + 
				"  Select b.call_number, title, number\r\n" + 
				"  From book as b\r\n" + 
				"  inner join(\r\n" + 
				"    Select call_number, Count(call_number) as number from copy\r\n" + 
				"    group by call_number\r\n" + 
				"  ) as c\r\n" + 
				"  on b.call_number = c.call_number\r\n" + 
				") as q\r\n" + 
				"inner join(\r\n" + 
				"  Select q.call_number, ifnull(c, 0) as borrow\r\n" + 
				"  from book as q\r\n" + 
				"  left join(\r\n" + 
				"    Select call_number, Count(*) as c\r\n" + 
				"    From checkout_record\r\n" + 
				"    where return_date is null\r\n" + 
				"    group by call_number\r\n" + 
				"  ) as t\r\n" + 
				"  on q.call_number = t.call_number\r\n" + 
				"  ) as t\r\n" + 
				" on t.call_number = q.call_number) as a\r\n"
				+ where;
		try {
			result = stmt.executeQuery(query);
			while(result.next()) {
				System.out.println("| " + result.getString(1) + " | " 
						+ result.getString(2) + " | " 
						+ table_author(result.getString(1)) + " | " 
						+ result.getString(3) + " |");
			}
		} catch (SQLException e) {
			System.out.println("[Error]: SQL Query Error");
		}
	}
	
	public static void db_showCheckoutRecord() {
		System.out.println("User: Show Checkout Record");
		reader.nextLine();
		System.out.print("Enter User ID: ");
		String uid = reader.nextLine();	
		System.out.println("| CallNum | CopyNum | Title | Author | Check-out | Returned? |");
		String query = "Select checkout_record.call_number, copy_number, title, checkout_date, CASE WHEN return_date is null THEN \"No\" ELSE \"Yes\" END as returned, user_id\r\n" + 
				"From checkout_record\r\n" + 
				"inner join book\r\n" + 
				"on checkout_record.call_number = book.call_number\r\n"
				+ "where user_id = '" + uid + "'\r\n"
						+ "order by checkout_date desc";
		try {
			result = stmt.executeQuery(query);
			while(result.next()) {
				System.out.println("| " + result.getString(1) + " | " 
						+ result.getString(2) + " | " 
						+ result.getString(3) + " | " 
						+ table_author(result.getString(1)) + " | " 
						+ result.getString(4) + " | " 
						+ result.getString(5) + " |");
			}
		} catch (SQLException e) {
			System.out.println("[Error]: SQL Query Error");
		}
	}

	
	public static void db_bookBorrowing() {
		System.out.println("Librarain: Book Borrowing");
		reader.nextLine();
		System.out.print("Enter User ID: ");
		String uid = reader.nextLine();	
		System.out.print("Enter Call Number: ");
		String call_number = reader.nextLine();	
		System.out.print("Enter Copy Number: ");
		String copy_number = reader.nextLine();	
		String query = "select * from(\r\n" + 
				"  select q.call_number, q.copy_number, ifnull(avaliable, 1) as avaliable\r\n" + 
				"  from copy as q\r\n" + 
				"  left join(\r\n" + 
				"    select call_number, copy_number, 0 as avaliable\r\n" + 
				"    from checkout_record\r\n" + 
				"    where return_date is null\r\n" + 
				"   ) as t\r\n" + 
				"   on q.call_number = t.call_number and q.copy_number = t.copy_number\r\n" + 
				") as q\r\n" + 
				"where call_number = '" + call_number + "' and copy_number = '" + copy_number +  "'";
		try {
			result = stmt.executeQuery(query);
			if(!result.next()) {
				System.out.println("[Error]: No Such Book Copy was found");
			}
			else {
				if(result.getString(3).equals("0")) {
					System.out.println("[Error]: Sorry, your target book copy has already been borrowed");
				}
				else {
					query = "Select * From(\r\n" + 
							"  Select q.user_id, max_books, ifnull(borrowed, 0) as borrowed, max_books - ifnull(borrowed, 0) as quota\r\n" + 
							"  from(\r\n" + 
							"    Select q.id as user_id, max_books\r\n" + 
							"    from user as q\r\n" + 
							"    inner join category as t\r\n" + 
							"    on t.id = q.category_id\r\n" + 
							"  ) as q\r\n" + 
							"  left join(\r\n" + 
							"    Select user_id, Count(*) as borrowed\r\n" + 
							"    from checkout_record\r\n" + 
							"    where return_date is null\r\n" + 
							"    group by user_id\r\n" + 
							"  ) as t\r\n" + 
							"  on q.user_id = t.user_id\r\n" + 
							") as q\r\n"
							+ "where user_id = '" + uid + "'";
					result = stmt.executeQuery(query);
					if(!result.next()) {
						System.out.println("[Error]: No Such User was found");
					}
					else {
						if(result.getString(4).equals("0")) {
							System.out.println("[Error]: Sorry, your are out of quota!");
						}
						else {
							DateFormat dateFormat = new SimpleDateFormat("yyyy/MM/dd");
							Date date = new Date();
							query = "Insert into checkout_record values('" + uid + "', '" + call_number + "', " + copy_number + " , '" + dateFormat.format(date) + "' , null);";
							stmt.executeUpdate(query);
							System.out.println("[OK]: Book checkout perform successfully!");
						}
					}	
				}
			}
		} catch (SQLException e) {
			System.out.println("[Error]: SQL Query Error");
		}
	}
	
	public static void db_bookreturning() {
		System.out.println("Librarain: Book Returning");
		reader.nextLine();
		System.out.print("Enter User ID: ");
		String uid = reader.nextLine();	
		System.out.print("Enter Call Number: ");
		String call_number = reader.nextLine();	
		System.out.print("Enter Copy Number: ");
		String copy_number = reader.nextLine();	
		String query = "Select * From checkout_record where user_id = '" + uid + "' and call_number = '" + call_number + "' and copy_number = '" + copy_number + "'";
		try {
			result = stmt.executeQuery(query);
			if(!result.next()) {
				System.out.println("[Error]: No Such Checkout Record was found");
			}
			else {
				if(result.getString(5) != null) {
					System.out.println("[Error]: Sorry, your target book copy has already been returned");
				}
				else {
					DateFormat dateFormat = new SimpleDateFormat("yyyy/MM/dd");
					Date date = new Date();
					query = "Update checkout_record set return_date = '" + dateFormat.format(date) + "' where user_id = '" + uid + "' and call_number =  '" + call_number + "' and  copy_number = " + copy_number;
					stmt.executeUpdate(query);
					System.out.println("[OK]: Book returning perform successfully!");
				}
			}
		} catch (SQLException e) {
			System.out.println("[Error]: SQL Query Error");
		}
	}
	
	public static void db_listUnreturnedBook() {
		//System.out.println("Librarian: List Unreturened Books");
		System.out.println("Librarian: List Unreturened Books");
		reader.nextLine();
		System.out.print("Type in the starting date [dd/mm/YYYY]: ");
		String start_date = reader.nextLine();
		start_date = dateFormat(start_date);
		System.out.print("Type in the ending date [dd/mm/YYYY]: ");
		String end_date = reader.nextLine();
		end_date = dateFormat(end_date);
		String query = "select CK.user_id, CK.call_number, CK.copy_number, CK.checkout_date\r\n" +
				"from checkout_record CK\r\n" +
				"where CK.return_date is null\r\n" +
				"and CK.checkout_date between " + "'" + start_date + "'" + " and " + "'" + end_date + "'\r\n"+
				"order by CK.checkout_date desc;";
		try {
			result = stmt.executeQuery(query);
			if(!result.next()) {
				System.out.println("No Un-returned Books in This Checkout Period");
			}
			else {
				System.out.println("|" + "User Id" + "|"+"Call number"+"|"+"Copy number"+"|"+"Checkout date"+"|");
				do {
					String user_id = result.getString(1);
					String call_number = result.getString(2);
					String copy_number = result.getString(3);
					String date = dbDateFormat(result.getString(4));
					System.out.println("|" + user_id + "|"+call_number+"|"+copy_number+"|"+date+"|");
				} while(result.next());
				System.out.println("[OK]: End of Query");
			}
		} catch (SQLException e) {
			System.out.println("[Error]: SQL Query Error");
		}
	}
	
	public static String table_author(String call_number) {
		String query = "Select name from author where call_number = '" + call_number + "'";	
		String author = "";
		try {
			ResultSet rs = stmt2.executeQuery(query);
			while (rs.next()) {
				author = author + rs.getString(1) + ",";
			}
		} catch (SQLException e) {
			System.out.println("[Error]: SQL Query Error");
		}
		return author;
	}
	
	public static String dateFormat(String date) {
		String return_date = "";
		try {
			String[] tmp_date = date.split("/");//dd/mm/yyyy
			String new_date = tmp_date[2] +"/"+ tmp_date[1] +"/"+ tmp_date[0];//yyyy/mm/dd
			return_date =  new_date;
		} catch (ArrayIndexOutOfBoundsException e) {
			System.out.println("[Error]: Input Date Format Error");
		}
		return return_date;
	}
	
	public static String dbDateFormat(String date) {
		String return_date = "";
		try {
			String[] tmp_date = date.split("-");//dd/mm/yyyy
			String new_date = tmp_date[2] +"/"+ tmp_date[1] +"/"+ tmp_date[0];//yyyy/mm/dd
			return_date =  new_date;
		} catch (ArrayIndexOutOfBoundsException e) {
			System.out.println("[Error]: Output Date Format Error");
		}
		return return_date;
	}
}