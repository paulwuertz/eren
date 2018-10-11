
function send() {
  $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });
}

function initCalendar(jar, renoj){
    //transformi json 2 calenderkonfirmajn datumojn
    var calendarEvents = [];
    for (var renInd in renoj) {
      var ren = renoj[renInd];
      if (ren.hasOwnProperty("periodo") && ren.periodo.hasOwnProperty("ektago")) {
        var d_ = '<dt><b><a href="'+ren.link+'">'+ren.nomo+'</a></b></dt>';
        d_+='<dt><b>Loko:</b></dt><dd>'+ren.loko+'</dd><dt><b>Tempo:</b></dt>';
        d_+='<dd>'+ ren.tempo+'</dd><dt><b>Priskribo:</b></dt><dd>'+ren.text+'</dd>';
        d_+='<dt><b>Kontakto:</b></dt><dd><a href="mailto:'+ren.mail+'">Alretpoŝtu!</a></dd>';
        evento = {
            title  : ren.nomo,
            start  : jar+'-'+ren.periodo.ekmonato+'-'+ren.periodo.ektago,
            description: d_
        }
        if (ren.periodo.fintago) {
          evento.end = jar+'-'+ren.periodo.finmonato+'-'+ren.periodo.fintago
        }
        calendarEvents.push(evento);
      }
    }

    //setup Calendar kaj aldonu eventojn
    $('#kalendaro').fullCalendar({
        locale:"eo",
        minDate: jar+"-01-01",
        maxDate: jar+"-12-31",
        header: {
            left: '',
            center: 'title',
            right: 'prev,next'
        },
        events: calendarEvents,
        eventRender: function(event, element) {
            element.qtip({
                content: event.description,
                hide: {
                    fixed: true,
                    delay: 300
                }
            });
        }
    }).fullCalendar( 'gotoDate', jar+"-01-01" );

    // set up the map
    map = new L.Map('mapo');

    // create the tile layer with correct attribution
    var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
    var osmAttrib='Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
    var osm = new L.TileLayer(osmUrl, {minZoom:3,attribution: osmAttrib});

    // start the map in South-East England -- de forega distanco ;)
    map.setView(new L.LatLng(51.3, 0.7),3);
    map.addLayer(osm);

    //plenigo de mapo kun JSON datumojn
    for (var ren in renoj) {
      if (ren.lat && ren.lon) {
        var marker = L.marker([ren.lat, ren.lon]).addTo(map);
        var m_str='<dt><b><a href="{{ ren.link }}">{{ ren.nomo }}</a></b></dt><dt><b>Loko:</b></dt><dd>{{ ren.loko }}</dd><dt><b>Tempo:</b></dt><dd>{{ ren.tempo }}</dd><dt><b>Priskribo:</b></dt><dd>{{ ren.text }}</dd><dt><b>Kontakto:</b></dt><dd><a href="mailto:{{ren.mail}}">Alretpoŝtu!</a></dd>'
        marker.bindPopup(m_str)
      }
    }
}
