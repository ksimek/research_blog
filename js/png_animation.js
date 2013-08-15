function construct_animation(element, image_urls)
{
    element = $(element);
    var img_div = $("<img/>");
    img_div.attr("src", image_urls[0]);

    var slider_div = $("<div/>");
    var num_images = image_urls.length;

    $(slider_div).slider({
        max: num_images-1,
        value: 1,
        slide: function(event, ui) {
        var value = ui.value;
        img_div.attr("src", image_urls[value]);
        }
    });

    element.append(img_div);
    element.append(slider_div);
}
