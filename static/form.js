jQuery.validator.addMethod("geocoordinates", function(value, element) {
    var latlng = value.split(",");
    var lat = (!isNaN(latlng[0]) && (latlng[0]<=90 && latlng[0]>=-90));
    var lng = (!isNaN(latlng[1]) && (latlng[1]<=180 && latlng[1]>=-180));
    return this.optional(element) || (latlng.length == 2 && lat && lng);
}, "Bonvole entajpu validajn geokordinatojn aux enklaku la mapon");

$.validator.addMethod("anyDate",
function(value, element) {
    return value.match(/^(0?[1-9]|[12][0-9]|3[0-1])[-](0?[1-9]|1[0-2])[-](20)\d{2}$/);
},"Bonvole entajpu validajn datoj por ek- kaj opcione por findato!");

function formData() {
    var geo=$('input[name="geoloc"]').val().split(","),
        lat = parseFloat(geo[0]),
        lng = parseFloat(geo[1]);
    return {
      "nomo":        $('input[name="eventnomo"]').val(),
      "organizanto": $('input[name="organizanto"]').val(),
      "grandeco":    $('select[name="grandeco"]').val(),
      "tipoj":       $('select[name="tipoj"]').val(),
      "ekdato":      $('input[name="ekdato"]').val(),
      "findato":     $('input[name="findato"]').val(),
      "lat":         lat,
      "lng":         lng,
      "lando":       $('input[name="lando"]').val(),
      "urbnomo":     $('input[name="urbnomo"]').val(),
      "website":     $('input[name="website"]').val(),
      "email":       $('input[name="email"]').val(),
      "priskribo":   $('textarea[name="priskribo"]').val(),
      "sekreta":     $('input[name="sekreta"]').val()
    }
}

//setup after HTML loaded
$(document).ready(function(){
    $('.datepicker').datepicker({format:"dd-mm-yyyy"});
    $('.in-opts select').formSelect();
    $('.tooltipped').tooltip({"exitDelay":1000});
    var l=$('#geoinput').leafletLocationPicker({
        alwaysOpen:true,
        mapContainer: "#map",
        locationDigits: 4,
        height: 250,
        map: {zoom:1}
    });
    var landData = {};
    var landoj=Object.values(BFHCountriesList)
    for(var l in landoj) landData[landoj[l]]=null;
    $('input.autocomplete').autocomplete({
      data: landData,
    });
    var formVal = $("form#novevento").validate({
      rules: {
        grandeco: {
          required: true,
          minlengt:1,
          valueNotEquals: "default"
        },
        tipoj: {
          required: true,
          minlengt:1
        },
        ekdato: {
            required: true,
            anyDate: true
        },
        findato: {
            required: false,
            anyDate: true
        },
        geoloc: {
            required: true,
            geocoordinates : true
        },
        website: {
            required: true,
            url: true
        },
        email: {
            required: true,
            email:true
        }
      },
      //For custom messages
       messages: {
       },
       errorElement : 'div',
       errorPlacement: function(error, element) {
         var placement = $(element).data('error');
         if (placement) {
           $(placement).append(error)
         } else {
           error.insertAfter(element);
         }
       },
      submitHandler: function(form) {
        //$(form).ajaxSubmit();
        $.ajax({ url: '/aldoniEventon',
          type: 'POST',
          beforeSend: function(xhr) {xhr.setRequestHeader('X-CSRF-Token', csrf_token)},
          data: formData(),
          always: function(response) {
            alert( "finished"+JSON.stringify(data));
            $('#someDiv').html(response);
          }
        });
      }
    });
    $("#idForm").submit(function(e) {
      event.preventDefault();
    });
    $("a#premo").click(function(event){
        event.preventDefault();
    });
}); //end document ready
