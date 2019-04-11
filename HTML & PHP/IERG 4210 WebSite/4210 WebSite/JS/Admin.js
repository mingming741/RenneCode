window.onload = function(){
    refresh();
}

function refresh(){
    refresh_inputForm();
}

function refresh_inputForm(){
    var operationValue = document.getElementById("operation").value;
    var tableValue = document.getElementById("table").value;
    
    if(operationValue == 1){ //Insert
        if(tableValue == 1){
            document.getElementById("bookNameLabel").textContent = "Book Name";
            document.getElementById("bookCategoryDiv").style.display= "block";
            document.getElementById("bookPriceDiv").style.display= "block";
            document.getElementById("bookDescDiv").style.display= "block";
            document.getElementById("inputFormPic").style.display= "block";
            document.getElementById("Spec").textContent = "Insert into 'Book': Choose a Category and input all other fields. Duplicate Book Name in same Category is not allowed. ";
            
        }
        else if(tableValue == 2){
            document.getElementById("bookNameLabel").textContent = "Category";
            document.getElementById("bookCategoryDiv").style.display= "none";
            document.getElementById("bookPriceDiv").style.display= "none";
            document.getElementById("bookDescDiv").style.display= "none";
            document.getElementById("inputFormPic").style.display= "none";
            document.getElementById("Spec").textContent = "Insert into 'Book Category': Input your Category Name. Duplicate Category Name in same Category is not allowed.";
        }
    }
    else if(operationValue == 2){ //Update
        if(tableValue == 1){
            document.getElementById("bookNameLabel").textContent = "Book Name";
            document.getElementById("bookCategoryDiv").style.display= "block";
            document.getElementById("bookPriceDiv").style.display= "block";
            document.getElementById("bookDescDiv").style.display= "block";
            document.getElementById("inputFormPic").style.display= "block";
            document.getElementById("Spec").textContent = "Update 'Book': Choose a Category and input a book name. All other field will be update to new input value.";
            
        }
        else if(tableValue == 2){
            document.getElementById("bookNameLabel").textContent = "Category";
            document.getElementById("bookCategoryDiv").style.display= "block";
            document.getElementById("bookPriceDiv").style.display= "none";
            document.getElementById("bookDescDiv").style.display= "none";
            document.getElementById("inputFormPic").style.display= "none";
            document.getElementById("Spec").textContent = "Update 'Book Category': Choose a category and input a new category name for this category. Duplicate Category Name in same Category is not allowed.";
        }
    }
    else if(operationValue == 3){ //Delete       
        document.getElementById("bookPriceDiv").style.display= "none";
        document.getElementById("bookDescDiv").style.display= "none";
        document.getElementById("inputFormPic").style.display= "none";
        if(tableValue == 1){
            document.getElementById("bookNameLabel").textContent = "Book Name";
            document.getElementById("bookCategoryDiv").style.display= "block";
             document.getElementById("Spec").textContent = "Delete 'Book': Choose a Category and input a Book name";
            
        }
        else if(tableValue == 2){
            document.getElementById("bookNameLabel").textContent = "Category";
            document.getElementById("bookCategoryDiv").style.display= "none";
            document.getElementById("Spec").textContent = "Delete 'Book Category': Input your Category Name.";
        }
    }
}

function operation_onChange(){
    refresh_inputForm();
}

function table_onChange(){
    refresh_inputForm();
}
