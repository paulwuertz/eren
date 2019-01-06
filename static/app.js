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

function renkontigxoJson2listo(ren) {
  var m_str  = "<dt><b>";
      m_str += "<a href='"
      m_str += url_for("konkretaEvento",ren.nomo);
      m_str += "'>"
      m_str += ren.nomo;
      m_str += '</a>'
  m_str += '</b></dt><dt>';
  m_str += '<b>Loko:</b></dt><dd>';
  if (ren.urbo && ren.posxtcodo) {
    m_str += ren.urbo + ", " ;
    m_str += ren.posxtcodo+ " - " + ren.lando;
  } else if (ren.regiono) {
    m_str += ren.regiono;
  } else {
    m_str += "-";
  }
  m_str += '</dd>';
  if (ren.hasOwnProperty("ektempo")){
      m_str += '<dt><b>Tempo:</b></dt><dd>';
      m_str += moment(ren.ektempo, "YYYY-MM-DD").format("Do MMMM YYYY");
      if (ren.hasOwnProperty("fintempo") && ren.fintempo!=""){
          m_str += ' - ' + moment(ren.fintempo, "YYYY-MM-DD").format("Do MMMM YYYY");
      }
      m_str += '</dd>';
  }
  if (ren.hasOwnProperty("priskribo") && ren.priskribo!="" && ren.priskribo!=null){
      m_str += '<dt><b>Priskribo:</b></dt><dd>';
      m_str += ren.priskribo;
  }
  if (ren.hasOwnProperty("ligilo" && ren.ligilo!="" && ren.ligilo!=null)){
      m_str += '<dt><b>Retejo:</b></dt><dd><a href="';
      m_str += ren.ligilo;
  }
  if (ren.hasOwnProperty("retposxto") && ren.retposxto!="" && ren.retposxto!=null){
      m_str += '<dt><b>Retposxta kontaktu:</b></dt><dd><a href="mailto:';
      m_str += ren.retposxto;
      m_str += '">Skribu la '+ ren.gxeneralaEvento +' teamo</a>';
      m_str += '</dd>';
  }
  return m_str;
}

function initCalendar(renoj){
    var query = getQueryParams(document.location.search);
    //transformi json 2 calenderkonfirmajn datumojn
    var calendarEvents = [];
    for (var renInd in renoj) {
      var ren = renoj[renInd];
      if (ren.hasOwnProperty("ektempo")) {
        var d_ = renkontigxoJson2listo(ren);
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

function url_for(route, nomo) {
    var getUrl = window.location;
    var baseUrl = getUrl.protocol + "//" + getUrl.host + "/";
    if(route=="aldoniEventon"){
        return baseUrl + "aldoniEventon"
    } else if(route=="konkretaEvento"){
        return baseUrl + "eventoj" + "/" + nomo
    } else if(route=="konkretajEventoj"){
        return baseUrl + "eventoj" + "/"
    } else if(route=="gxeneralaEvento"){
        return baseUrl + "evento" + "/" + nomo
    } else if(route=="gxeneralajEventoj"){
        return baseUrl + "evento" + "/"
    } else if(route=="organizacio"){
        return baseUrl + "organizacioj" + "/" + nomo
    } else if(route=="organizacioj"){
        return baseUrl + "organizacioj" + "/"
    } else if(route=="static"){
        return baseUrl + "static" + "/" + nomo
    } else {
      return baseUrl
    }
}

function initMapo(renoj){
    // set up the map
    map = new L.Map('mapo');

    // create the tile layer with correct attribution
    var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
    var osmAttrib='Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
    var osm = new L.TileLayer(osmUrl, {minZoom:2,attribution: osmAttrib});

    map.setView(new L.LatLng(0, 0),2);
    map.addLayer(osm);

    //plenigo de mapo kun JSON datumojn
    for (var renInd in renoj) {
      var ren = renoj[renInd];
      if (ren.hasOwnProperty("lat") && ren.lat != null) {
        var marker = L.marker([ren.lat, ren.lon]).addTo(map);
        var m_str  = renkontigxoJson2listo(ren);
        marker.bindPopup(m_str)
      }
    }
    return map;
}

$(document).ready(function(){
    moment.locale('eo');
});
