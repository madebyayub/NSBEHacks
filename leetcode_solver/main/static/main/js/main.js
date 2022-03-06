window.addEventListener("load", function(){
    var minNumber = 1; // The minimum number you want
    var maxNumber = 300; // The maximum number you want
    var randomnumber = Math.floor(Math.random() * (maxNumber + 1) + minNumber); // Generates random number
    var str = randomnumber.toString()
    console.log(randomnumber);
    $('#random').attr("href", "problem/" + str); // Sets content of <div> to number
    return false; // Returns false just to tidy everything up
});
