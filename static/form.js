jQuery.validator.addMethod("geocoordinates", function(value, element) {
    var latlng = value.split(",");
    var lat = (!isNaN(latlng[0]) && (latlng[0]<=90 && latlng[0]>=-90));
    var lng = (!isNaN(latlng[1]) && (latlng[1]<=180 && latlng[1]>=-180));
    return this.optional(element) || (latlng.length == 2 && lat && lng);
}, "Bonvole entajpu validajn geokordinatojn aux enklaku la mapon");

//setup after HTML loaded
$(document).ready(function(){
    $('.datepicker').datepicker();
    $('.in-opts select').formSelect();
    $('.tooltipped').tooltip({"exitDelay":1000});
    var l=$('#geoinput').leafletLocationPicker(
      {
        alwaysOpen:true,
        mapContainer: "#map",
        locationDigits: 4,
        height: 250,
        map: {zoom:1}
      }
    ).on('changeLocation', function(e) {
        $('#geolat').val( e.latlng.lat )
        $('#geolng').val( e.latlng.lng )
    });	;
    var landData = {};
    var landoj=Object.values(BFHCountriesList)
    for(var l in landoj) landData[landoj[l]]=null;
    $('input.autocomplete').autocomplete({
      data: landData,
    });
    var formVal = $("#novevento").validate({
      rules: {
        grandeco: {
          minlengt:1
        },
        tipoj: {
          minlengt:1
        },
        grandeco: {
          valueNotEquals: "default"
        },
        ekdato: {
            required: true,
            date: true
        },
        findato: {
            required: true,
            date: true
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
        var formData = {
          "organizanto": $('input[name="organizanto"]').val(),
          "grandeco":    $('input[name="grandeco"]').val(),
          "tipoj":       $('input[name="tipoj"]').val(),
          "ekdato":      $('input[name="ekdato"]').val(),
          "findato":     $('input[name="findato"]').val(),
          "geoloc":      $('input[name="geoloc"]').val(),
          "lando":       $('input[name="lando"]').val(),
          "urbnomo":     $('input[name="urbnomo"]').val(),
          "website":     $('input[name="website"]').val(),
          "email":       $('input[name="email"]').val(),
          "description": $('input[name="description"]').val(),
          "sekreta":     $('input[name="sekreta"]').val()
        }

        $.ajax({ url: '/aldoniEventon',
          type: 'POST',
          beforeSend: function(xhr) {xhr.setRequestHeader('X-CSRF-Token', csrf_token)},
          data: formData,
          always: function(response) {
            alert( "finished"+JSON.stringify(data));
            $('#someDiv').html(response);
          }
        });
      }
    })
    $("a#premo").click(function(event){
        event.preventDefault();
        //formVal.form();
      });
    })
