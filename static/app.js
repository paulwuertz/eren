function getQueryParams(qs) {
    qs = qs.split('+').join(' ');

    var params = {},
        tokens,
        re = /[?&]?([^=]+)=([^&]*)/g;

    while (tokens = re.exec(qs)) {
        params[decodeURIComponent(tokens[1])] = decodeURIComponent(tokens[2]);
    }

    return params;
}

function send() {
  $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });
}

function initCalendar(renoj){
    var query = getQueryParams(document.location.search);
    //transformi json 2 calenderkonfirmajn datumojn
    var calendarEvents = [];
    for (var renInd in renoj) {
      var ren = renoj[renInd];
      if (ren.hasOwnProperty("ektempo")) {
        var d_ = '<dt><b><a href="'+ren.link+'">'+ren.nomo+'</a></b></dt>';
        d_+='<dt><b>Loko:</b></dt><dd>'+ren.loko+'</dd><dt><b>Tempo:</b></dt>';
        d_+='<dd>'+ ren.tempo+'</dd><dt><b>Priskribo:</b></dt><dd>'+ren.text+'</dd>';
        d_+='<dt><b>Kontakto:</b></dt><dd><a href="mailto:'+ren.mail+'">Alretpoŝtu!</a></dd>';
        evento = {
            title  : ren.nomo,
            start  : ren.ektempo,
            description: d_
        }
        if (ren.hasOwnProperty("fintempo")) {
          evento.end = ren.fintempo
        }
        calendarEvents.push(evento);
      }
    }

    //setup Calendar kaj aldonu eventojn
    $('#kalendaro').fullCalendar({
        locale:"eo",
        minDate: query["ektempo"],
        maxDate: query["fintempo"],
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
    }).fullCalendar( 'gotoDate', query["ektempo"] );
}
function initMapo(renoj){
    // set up the map
    map = new L.Map('mapo');

    // create the tile layer with correct attribution
    var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
    var osmAttrib='Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
    var osm = new L.TileLayer(osmUrl, {minZoom:2,attribution: osmAttrib});

    // start the map in South-East England -- de forega distanco ;)
    map.setView(new L.LatLng(51.3, 0.7),3);
    map.addLayer(osm);

    //plenigo de mapo kun JSON datumojn
    for (var renInd in renoj) {
      var ren = renoj[renInd];
      if (ren.hasOwnProperty("lat") && ren.lat!="None") {
        var marker = L.marker([ren.lat, ren.lon]).addTo(map);
        var m_str="<dt><b><a href="
            m_str += ren.ligilo;
            m_str += ">" + ren.nomo;
            m_str += '</a></b></dt><dt>';
            m_str += '<b>Loko:</b></dt><dd>';
            if (ren.urbo && ren.posxtcodo) {
              m_str += ren.urbo + ", " ;
              m_str += ren.posxtcodo+ " - " + ren.lando;
            } else if (ren.regiono) {
              m_str += ren.regiono;
            } else {
              m_str += "-";
            }
            m_str += '</dd><dt><b>Tempo:</b></dt><dd>';
            m_str += ren.ektempo;
            m_str += '</dd><dt><b>Priskribo:</b></dt><dd>';
            m_str += ren.priskribo;
            m_str += '</dd><dt><b>Kontakto:</b></dt><dd><a href="mailto:';
            m_str += ren.retposxto;
            m_str += '>Alretpoŝtu!</a></dd>';
        marker.bindPopup(m_str)
      }
    }
    return map;
}
