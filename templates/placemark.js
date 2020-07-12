ymaps.ready(init);

function init() {
    var myMap = new ymaps.Map("map", {
            center: [57.152871, 33.121689],
            zoom: 14,
            controls: []
        }, {
            searchControlProvider: 'yandex#search'
        });

    myMap.geoObjects
        {% for marker in markers_list %}

        .add(new ymaps.Placemark([ {{marker.longitude}}, {{marker.latitude}} ], {
            balloonContent: '<a href="{{marker.place_url}}">{{marker.name}}</a>'
        }, {
            iconColor: '#0095b6'
        }))

        {% endfor %};
}
