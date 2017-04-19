onmessage = function(e){
    this.h = e.data[0];
    this.pixel = e.data[1];
    this.w = e.data[2];
    this.x = e.data[3];
    this.y = e.data[4];
    hs = e.data[5];
    data = e.data[6];
    this.alpha = e.data[7];
    
    result = {rgbas: [], rect: []};

    for (y = 0; y <= this.h + hs; y += this.pixel) {
        yy = y;
        result.rgbas.push([])
        result.rect.push([])
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
            result.rgbas[y/this.pixel].push(rgba);
            result.rect[y/this.pixel].push([(this.x + x) - hs, (this.y + y) - hs, this.pixel, this.pixel]);
        }
    }

    postMessage(result);

}