window.onload = function(){
    reload_Cart();
}

function reload_Cart() {
    var tempCart;
    if(localStorage.cart != undefined){
        tempCart = JSON.parse(localStorage.cart);
    }
    var content = "<table> <tr> <th> Product </th> <th> Price </th> <th> Count </th> <th> Total </th> </tr>";
    var total = 0;
    var totalForOnePro = 0;
    for (var p in tempCart){
        totalForOnePro = tempCart[p].num * tempCart[p].price;
        content += "<tr><td>" + tempCart[p].name + "</td> <td>$" + tempCart[p].price + "</td>" +         
            "<td><input type=\"text\"  value=" + tempCart[p].num + " oninput=\"updatePrice(" + p + ",this.value)\" /></td>" +
            "<td>$"+totalForOnePro+"</td>";
        total += totalForOnePro;
    }
    content += "</table>";
    content += "Total: $"+total;
    
    var form = "<form id=\"payForm\" action=\"https://www.sandbox.paypal.com/cgi-bin/webscr\" method=\"POST\" onsubmit=\"return cart_submit(this)\">";
    form += "<input type=\"hidden\" name=\"cmd\" value=\"_cart\">";
    form += "<input type=\"hidden\" name=\"upload\" value=\"1\">";
    form += "<input type=\"hidden\" name=\"business\" value=\"419955347bus@qq.com\">";
    form += "<input type=\"hidden\" name=\"currency_code\" value=\"HKD\">";
    form += "<input type=\"hidden\" name=\"charset\"  value=\"utf-8\">";

    var list_num = 1;
    for (var p1 in tempCart){
        form += "<input type=\"hidden\" name=\"item_name_"+ list_num +"\" value=\""+ tempCart[p1].name +"\"  >" ; //product name
        form += "<input type=\"hidden\" name=\"item_number_"+ list_num +"\" value=\""+ p1 + "\" >"; //product reference number
        form += "<input type=\"hidden\" name=\"quantity_"+ list_num +"\" value=\""+ tempCart[p1].num +"\" >"; //product count
        form += "<input type=\"hidden\" name=\"amount_"+ list_num +"\" value=\""+ tempCart[p1].price +"\"  >" ; //product price
        list_num += 1;
    }
    form += "<input type=\"hidden\" name=\"custom\" value=\"\">";
    form += "<input type=\"hidden\" name=\"invoice\" value=\"\">";
    form += "<input type=\"submit\" id=\"checkout\" value=\"Checkout\"></form> ";
    content += form;
    
    document.getElementById("shoppingCart").innerHTML = content;
}

function ajaxSend(){
    var xmlhttp =  new XMLHttpRequest();
    xmlhttp.onreadystatechange = function()  {
        if (xmlhttp.readyState ==  4  &&  xmlhttp.status  ==  200)    {
            var obj = JSON.parse(xmlhttp.responseText);
            if (obj.ifLogin == 0) {
                alert("You should login first ^_^");
                window.location.href = "Login.php";
            }
            else {
                var form = document.getElementById("payForm");
                form.elements.namedItem("invoice").value = obj.id;
                form.elements.namedItem("custom").value = obj.digest;
                form.submit();
                ClearCart();
            }
        }
    };

    xmlhttp.open("POST",  "getOrder.php", true);
    xmlhttp.setRequestHeader("Content-type",  "application/x-www-form-urlencoded");
    var tempCart = JSON.parse(localStorage.cart);
    var pair = {};
    for (var tp in tempCart) {
        pair[tp] = tempCart[tp].num;
    }
    pair = JSON.stringify(pair);
    var message = "message=" + pair;
    xmlhttp.send(message);
}

function cart_submit(e) {
    reload_Cart();
    var tempCart = JSON.parse(localStorage.cart);
    var products = {};
    var index = 0;
    for (var product in tempCart) {
        products[index] = product;
        index = index + 1;
    }
    if (index == 0){
        alert("No product to purchase !");
        return false;
    }
    else {
        ajaxSend();
    }
    return false;
}

function addToCart(pid) {
    myLib.get({action:'prod_fetchByPid', pID: pid}, function(json){
        var cart = localStorage.cart;
        if (cart == undefined)
            cart = {};
        else
            cart = JSON.parse(cart);
        if(cart[pid] == undefined)
            cart[pid] = {'num':0};
        cart[pid].name = json[0].Name.escapeHTML();
        cart[pid].price = json[0].Price.escapeHTML();
        cart[pid].num = cart[pid].num + 1;
        localStorage.cart = JSON.stringify(cart);
        reload_Cart();
    });
}

function updatePrice(p, number) {
    var tempCart = JSON.parse(localStorage.cart);
    if(number > 0){
        tempCart[p].num = number;
        localStorage.cart = JSON.stringify(tempCart);
    }
    else if(number == 0) {
        delete tempCart[p];
        localStorage.cart = JSON.stringify(tempCart);
    }
    reload_Cart();
}

function ClearCart() {
    localStorage.clear();
    reload_Cart();
}

