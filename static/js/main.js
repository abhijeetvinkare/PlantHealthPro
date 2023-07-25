$(document).ready(function () {
  // Init
  $(".image-section").hide();
  $(".loader").hide();
  $("#result").hide();
  $("#description").hide();

  // Upload Preview
  function readURL(input) {
    if (input.files && input.files[0]) {
      var reader = new FileReader();
      reader.onload = function (e) {
        $("#imagePreview").css(
          "background-image",
          "url(" + e.target.result + ")"
        );
        $("#imagePreview").hide();
        $("#imagePreview").fadeIn(650);
      };
      reader.readAsDataURL(input.files[0]);
    }
  }
  $("#imageUpload").change(function () {
    $(".image-section").show();
    $("#btn-predict").show();
    $("#result").text("");
    $("#result").hide();
    $("#description").hide(); // hide description when new image is uploaded
    readURL(this);
  });

  // Predict
  $("#btn-predict").click(function () {
    var form_data = new FormData($("#upload-file")[0]);

    // Show loading animation
    $(this).hide();
    $(".loader").show();

    // Make prediction by calling api /predict
    $.ajax({
      type: "POST",
      url: "/predict",
      data: form_data,
      contentType: false,
      cache: false,
      processData: false,
      async: true,
      success: function (data) {
        // Get and display the result
        $(".loader").hide();
        $("#result").fadeIn(600);
        $("#result").text(" Result:  " + data);

        // Show description based on predicted class
        if (data === "Grassy Shoots") {
          $("#description").text(
            "Remedies : Your plant is in the grassy shoots stage, which is a normal part of plant growth. Keep providing adequate sunlight and water, and your plant will soon enter the vegetative stage."
          );
        } else if (data === "Healthy") {
          $("#description").text(
            "Remedies : Your plant looks healthy! Keep providing adequate sunlight and water, and you should soon see fruiting."
          );
        } else if (data === "Mites") {
          $("#description").text(
            "Remedies : Your plant has been infested with mites. This can be treated by spraying the plant with insecticidal soap or neem oil. Make sure to treat the plant several times to completely eradicate the mites."
          );
        } else if (data === "Ring Spot") {
          $("#description").text(
            "Remedies : Your plant has been infected with ring spot virus, which is a fungal disease. Remove any infected leaves and destroy them, and spray the plant with a fungicide. Keep the plant dry and avoid overhead watering to prevent further spread of the disease."
          );
        } else if (data === "YLD") {
          $("#description").text(
            "Remedies : Your plant is suffering from yellow leaf disease, which is caused by a deficiency in nutrients such as nitrogen or magnesium. Fertilize the plant with a balanced fertilizer, and make sure it is receiving adequate water and sunlight."
          );
        }

        $("#description").show(); // show description after result is displayed
        
        console.log("Success!");
      },
    });
  });
});

// navbar

// define all UI variable
const navToggler = document.querySelector(".nav-toggler");
const navMenu = document.querySelector(".site-navbar ul");
const navLinks = document.querySelectorAll(".site-navbar a");

// load all event listners
allEventListners();

// functions of all event listners
function allEventListners() {
  // toggler icon click event
  navToggler.addEventListener("click", togglerClick);
  // nav links click event
  navLinks.forEach((elem) => elem.addEventListener("click", navLinkClick));
}

// togglerClick function
function togglerClick() {
  navToggler.classList.toggle("toggler-open");
  navMenu.classList.toggle("open");
}

// navLinkClick function
function navLinkClick() {
  if (navMenu.classList.contains("open")) {
    navToggler.click();
  }
}
