// Serial code

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
          // Handle the config
          hs = ~~(this.pixel / 2) ;
          this.pixel = this.pixel || 10;
          this.x = this.x || 0;
          this.y = this.y || 0;
          this.w = this.w || this.image.width;
          this.h = this.h || this.image.height;
          this.alpha = this.alpha || 1;
          this.clean = this.clean || false;

          // Canvas related stuff goes in the main thread
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

          // Spin up a new worker
          var worker = new Worker("pix.js");
          
          var canvas = document.createElement('canvas');

          worker.postMessage([this.h , this.pixel, this.w, this.x, this.y, hs, data, this.alpha]); // Sending message as an array to the worker
          // Create a copy for the onmessage handler
          var pxo = this;

          // Wait for the message from the worker
          worker.onmessage = function(e) {
                console.log(pxo._context)
                // Another nested for loop to apply results
                for (y = 0; y <= pxo.h + hs; y += pxo.pixel) {
                    for (x = 0; x <= pxo.w + hs; x += pxo.pixel) {
                        // Apply the results through the pxo object
                        pxo[this.clean ? '_contextClean' : '_context'].fillStyle = e.data.rgbas[y/10][x/10];
                        pxo[this.clean ? '_contextClean' : '_context']
                            .fillRect( (pxo.x + x) - hs, (pxo.y + y) - hs, pxo.pixel, pxo.pixel )
                    }
                }
                // replace the original iamge with pixellated image
                pxo.replace();
            };


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