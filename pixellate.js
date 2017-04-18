(function() {
    "use strict";

    window.Pixelify = Pixelify;

    function Pixelify(image, config) {
        if (!image) return
        this.image = image;

        // test canvas support
        var canvas = document.createElement('canvas')
        if (!(canvas.getContext && canvas.getContext('2d'))) return

        // canvas is supported
        this._canvas = canvas;

        for (var prop in config) {
            if (config.hasOwnProperty(prop)) {
                this[prop] = config[prop];
            }
        }

        this.init(config);
    };

    Pixelify.prototype = {

        init : function init(config) {
            // wait until the image is available for manipulation
            var imageLoaded = function imageLoaded() {
                this.image.onload = null;
                this.pixelate(config);
            }.bind(this);

            this.image.onload = imageLoaded;

            if (this.image.complete) this.image.onload();
        },

        pixelate : function pixelate(config) {
            var x, y, xx, yy, image_index, r, g, b, a, rgba, data, imageData, hs;


            hs = ~~(this.pixel / 2) ;
            this.pixel = this.pixel || 10;
            this.x = this.x || 0;
            this.y = this.y || 0;
            this.w = this.w || this.image.width;
            this.h = this.h || this.image.height;
            this.alpha = this.alpha || 1;
            this.clean = this.clean || false;

            this._context       = this._canvas.getContext('2d');
            this._canvas.width  = this.image.width;
            this._canvas.height = this.image.height;

            // draw image on canvas
            this._context.drawImage(this.image, 0, 0);

            // get image data
            data = this._context.getImageData(this.x, this.y, this.w, this.h).data;

            // clean on version canvas version
            if (this.clean) {
                this._canvasClean       = document.createElement('canvas');
                this._contextClean      = this._canvasClean.getContext('2d');
                this._canvasClean.width = this._canvas.width;
                this._canvasClean.height= this._canvas.height;
            }

            for (y = 0; y <= this.h + hs; y += this.pixel) {
                yy = y;
                if (yy >= this.h) yy = this.h - this.pixel + hs;

                for (x = 0; x <= this.w + hs; x += this.pixel) {
                    xx = x;
                    if (xx >= this.w) xx = this.w - this.pixel + hs;

                    image_index = (yy * (this.w * 4)) + (xx * 4);

                    r = data[image_index];
                    g = data[image_index + 1];
                    b = data[image_index + 2];
                    a = (this.alpha * data[image_index + 3]) / 255;

                    rgba = 'rgba(' + r +','+ g +','+ b +','+ a + ')';

                    this[this.clean ? '_contextClean' : '_context'].fillStyle = rgba;
                    this[this.clean ? '_contextClean' : '_context']
                        .fillRect( (this.x + x) - hs, (this.y + y) - hs, this.pixel, this.pixel )
                }
            }

            this.replace();
            return this;
        },

        _getDataURL : function _getDataURL() {
            return this[(this.clean) ? "_canvasClean" : "_canvas"].toDataURL("image/png");
        },

        replace : function replace() {
            this.image.setAttribute('src', this._getDataURL());
            return this;
        },

        save : function save() {
            var url = this._getDataURL(),
                w   = this.image.width,
                h   = this.image.height;

            window.open(url, "Pixelify", "width=" + w + ",height=" + h + "");
        }
    };
}());