ymaps.ready(init);

function init() {
    var myMap = new ymaps.Map("map", {
            center: [55.76, 37.64],
            zoom: 10
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
