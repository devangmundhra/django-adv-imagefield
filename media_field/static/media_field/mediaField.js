window.onload = function(){
/* Creating an ability to format a String */
if(!String.prototype.format) {
    var format = function() {
        var args = arguments;
        var result = this.replace(/{(\d+)}/g, function(match, number) {
            return typeof args[number] != 'undefined' ? args[number] : match;
        })

        return result;
    }
    String.prototype.format = format;
};

var nextPage = function(callback) {
    if(this.page < this.pages) {
        this.page += 1;
    }
};
var prevPage = function() {
    if(this.page > 1) {
        this.page -= 1;
    }
};
var getPhotos = function() {
    return this.photos;
};
var googleNextPage = function(){
    this.page += 1;
    this.start += 8;
};

var googlePrevPage = function(){
    if(this.page > 1){
        this.page -= 1;
        this.start -= 8;
    }
};

var getGooglePhotos = function() {
    return this.photos;
};



var loadJSON = function(url, success, error) {
    var ajax = new XMLHttpRequest();
    var processResponse = function(){
        if(success && ajax.status == 200 && ajax.readyState == 4){
            return success(ajax.responseText);
        };
        if(error || ajax.status == 404 && ajax.readyState == 4) {
            return error(ajax.responseText);
        }
    };
    ajax.onreadystatechange = processResponse;
    ajax.open("GET", url, true);
    ajax.send();
};

var jsonGoogleApi = function(response){
    var response = JSON.parse(response);
    var data = response.items;
    if(!data){
        console.log('There is no data from Google');
        return;
    }
    images.google.start = response.queries.request[0].startIndex;
    images.google.pages = Math.ceil(Number(response.queries.request[0].totalResults)/8);
    images.google.photos = [];
    for(var i=0; i < data.length; i++){
        var p = data[i];
        var photo = {};
        photo.url = p.link;
        // thumbnail width 150
        photo.thumbnail = p.image.thumbnailLink;
        images.google.photos.push(photo);
    };
};

var jsonFlickrApi = function(response){
    if(response.stat != "ok"){
        alert('Unable to get photos from Flickr:' + response.message);
        return;
    }
    var data = response.photos;
    images.flickr.pages = Math.ceil(Number(data.total)/8);
    images.flickr.photos = [];
    for(var i=0; i < data.photo.length; i++){
        var p = data.photo[i];
        var photo = {};
        photo.url = "https://farm{0}.staticflickr.com/{1}/{2}_{3}.jpg".format(p.farm, p.server, p.id, p.secret);
        // t for thumbnail, 100 on longest side
        photo.thumbnail = "https://farm{0}.staticflickr.com/{1}/{2}_{3}_{4}.jpg".format(p.farm, p.server, p.id, p.secret, "q");
        images.flickr.photos.push(photo);
    };
};

var jsonUrlApi = function(response){
    var data = JSON.parse(response);
    if(data.status != "ok"){
        alert('Unable to get photos from your url');
        return;
    }
    data = data.urls;
    for(var i=0; i<data.length; i++){
        data[i].thumbnail = data[i].url;
    };
    images.url.pages = Math.ceil(data.length / 8);
    images.url.photos = data;
}

var constructUrl = function(type){
    if(type == 'flickr'){
        return "https://api.flickr.com/services/rest/?" +
            "method=flickr.photos.search" +
            "&api_key=" + FLICKR_API_KEY +
            "&format=json" +
            "&license=1,2,3,4,5,6,7" +
            "&sort=relevance" +
            "&media=photos" +
            "&per_page=8" +
            "&page=" + images.flickr.page +
            "&text=" + images.query;
    };
    if(type == 'google'){
        return "https://www.googleapis.com/customsearch/v1?" +
            "key=" + GOOGLE_API_KEY + 
            "&cx=" + GOOGLE_SENGINE_ID +
            "&searchType=image" +
            "&imgType=photos" +
            "&num=8" +
            "&start=" + images.google.start +
            "&safe=high" +
            "&rights=cc_publicdomain,cc_attribute,cc_sharealike,cc_noncommercial,cc_nonderived" +
            "&q=" + images.query;
    };
    if(type == 'url'){
        return MEDIA_FIELD_API + "?url=" + encodeURIComponent(images.url.query);
    }
};

var querySearch = function(type, callback) {
    var url = constructUrl(type);
    loadJSON(url, function(data){
        if(callback){
            callback(data);
        }
    });
};

var images = {
    query: '',
    flickr: {
        page: 1,
        pages: 0,
        nextPage: nextPage,
        prevPage: prevPage,
        getPhotos: getPhotos,
        photos: [],
        sync: function(callback){
            querySearch('flickr',function(data){
                eval(data);
                if(callback){
                    callback(data);
                }
            });
        }
    },
    google: {
        page: 1,
        start: 1,
        pages: 0,
        nextPage: googleNextPage,
        prevPage: googlePrevPage,
        getPhotos: getGooglePhotos,
        photos: [],
        sync: function(callback){
            querySearch('google',function(data){
                jsonGoogleApi(data);
                if(callback){
                    callback(data);
                }
            });
        }
    },
    url: {
        query: '',
        page: 1,
        pages: 0,
        photos: [],
        nextPage: function(){
            if(this.pages > this.page){
                this.page += 1;
            }
        },
        prevPage: function(){
            if(this.page > 1){
                this.page -= 1;
            }
        },
        getPhotos: function(){
            var start = (this.page - 1) * 8;
            var end = (this.page * 8) < this.photos.length ? (this.page * 8) : this.photos.length;
            return this.photos.slice(start, end);
        },
        sync: function(callback){
            querySearch('url', function(data) {
                jsonUrlApi(data);
                if(callback){
                    callback(data);
                }
            });
        }
    }
};


var view = {};
view.search = {};
view.url = {};
view.image = document.getElementById('media_widget_image');
view.image_hidden = document.getElementById('media_widget_image_hidden');
view.search.button = document.getElementById('searchButton');
view.search.input = document.getElementById('searchInput');
view.url.button = document.getElementById('urlButton');
view.url.input = document.getElementById('urlInput');
view.search.wrapper = document.getElementById('flickr_google_wrapper');
view.url.wrapper = document.getElementById('url_wrapper');

view.search.button.onclick = function(e) {
    e.preventDefault();
    var query = view.search.input.value;
    images.query = query;
    images.flickr.page = 1;
    images.google.page = 1;
    images.flickr.sync(function(data){
       view.search.drawWrapper();
       view.drawThumbnails(images.flickr.getPhotos(), view.search.ul);
        view.search.page.innerHTML = images.flickr.page + " of " + images.flickr.pages;
    });
    images.google.sync();
};
view.url.button.onclick = function(e) {
    e.preventDefault();
    images.url.query = view.url.input.value;
    images.url.page = 1;
    images.url.sync(function(data){
        view.url.drawWrapper();
        view.drawThumbnails(images.url.getPhotos(), view.url.ul);
        view.url.page.innerHTML = images.url.page + " of " + images.url.pages;
    });
};

view.search.drawWrapper = function() {
    view.search.wrapper.innerHTML = '<div class="media_widget_row" style="text-align:center;">' +
                    '<input type="radio" name="search" value="flickr" id="flickr" checked>Flickr ' +
                    '<input type="radio" name="search" value="google" id="google">Google' +
                '</div>' +
                '<ul id="flickr_google" class="media_widget_thumbnails" style="margin-left:0px;margin-bottom:0px;padding-left:0px;">' +
                '</ul>' +
                '<div class="media_widget_row" style="text-align:center;">' +
                    '<a id="flickr_google_prev" href="#">&lt;prev</a>' +
                    ' page <span id="flickr_google_page"></span> ' +
                    '<a id="flickr_google_next" href="#">next&gt;</a>' +
                '</div>';
    view.search.ul = document.getElementById('flickr_google');
    view.search.next = document.getElementById('flickr_google_next');
    view.search.prev = document.getElementById('flickr_google_prev');
    view.search.page = document.getElementById('flickr_google_page');
    view.search.flickr = document.getElementById('flickr');
    view.search.google = document.getElementById('google');

    view.search.next.onclick = function(e) {
        e.preventDefault();

        if(view.search.flickr.checked){
            images.flickr.nextPage();
            images.flickr.sync(function(data){
                view.drawThumbnails(images.flickr.getPhotos(), view.search.ul);
                view.search.page.innerHTML = images.flickr.page + " of " + images.flickr.pages;
            });
        } else{
            images.google.nextPage();
            images.google.sync(function(data){
               view.drawThumbnails(images.google.getPhotos(), view.search.ul);
                view.search.page.innerHTML = images.google.page + " of " + images.google.pages;
            });
        };
    };
    view.search.prev.onclick = function(e) {
        e.preventDefault();
        var photos = [];
        if(view.search.flickr.checked){
            images.flickr.prevPage();
            images.flickr.sync(function(data){
               view.drawThumbnails(images.flickr.getPhotos(), view.search.ul);
                view.search.page.innerHTML = images.flickr.page + " of " + images.flickr.pages;
            });
        } else{
            images.google.prevPage();
            images.google.sync(function(data){
               view.drawThumbnails(images.google.getPhotos(), view.search.ul);
                view.search.page.innerHTML = images.google.page + " of " + images.google.pages;
            });
        };
    };
    view.search.flickr.onclick = function(){
        var photos = images.flickr.getPhotos();
        view.search.page.innerHTML = images.flickr.page + " of " + images.flickr.pages;
        view.drawThumbnails(photos, view.search.ul);
    };
    view.search.google.onclick = function(){
        var photos = images.google.getPhotos();
        view.search.page.innerHTML = images.google.page + " of " + images.google.pages;
        view.drawThumbnails(photos, view.search.ul);
    };
};
view.url.drawWrapper = function() {
    view.url.wrapper.innerHTML = '<ul id="url" class="media_widget_thumbnails" style="margin-left:0px;margin-bottom:0px;padding-left:0px;">' +
                '</ul>' +
                '<div class="media_widget_row" style="text-align:center;">' +
                    '<a id="url_prev" href="#">&lt;prev</a>' +
                    ' page <span id="url_page">1</span> ' +
                    '<a id="url_next" href="#">next&gt;</a>' +
                '</div>';
    view.url.ul = document.getElementById('url');
    view.url.next = document.getElementById('url_next');
    view.url.prev = document.getElementById('url_prev');
    view.url.page = document.getElementById('url_page');


    view.url.next.onclick = function(e) {
        e.preventDefault();
        images.url.nextPage();
        var photos = images.url.getPhotos();
        view.drawThumbnails(photos, view.url.ul);
        view.url.page.innerHTML = images.url.page + " of " + images.url.pages;
    };
    view.url.prev.onclick = function(e) {
        e.preventDefault();
        images.url.prevPage();
        var photos = images.url.getPhotos();
        view.drawThumbnails(photos, view.url.ul);
        view.url.page.innerHTML = images.url.page + " of " + images.url.pages;
    };

};

view.drawThumbnails = function(photos, ul){
    var li = ' <li style="list-style-type:none; display:inline;">' +
        '<a href="#"><img id="thumbnail_{0}" class="media_widget_thumbnail" src="{1}" style="width:150px;"></a>' +
        '</li>';
    var thumbnails = '';
    for(var i = 0; i < photos.length; i++){
        thumbnails += li.format(i, photos[i].thumbnail);
    }
    if(photos.length == 0){
        thumbnails = "There is nothing found."
    }
    ul.innerHTML = '';
    ul.innerHTML = thumbnails;

    var onThumbnailClick = function(photo){
        return function(e){
            e.preventDefault();
            view.image.src = photo.url;
            view.image_hidden.value = photo.url;
        };
    };

    var thumbnails = ul.getElementsByClassName('media_widget_thumbnail');
    for(var i=0; i<thumbnails.length; i++){
        thumbnails[i].onclick = onThumbnailClick(photos[i]);
    }
};
};
