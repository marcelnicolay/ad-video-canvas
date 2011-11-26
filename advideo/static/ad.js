/*jslint devel: false, browser: true, sloppy: true, safe: true,
 plusplus: true, fragment: true, maxerr: 50, maxlen: 80, indent: 4 */
/*global $: true, sendMultipleFiles: true */

$(document).ready(function () {
    var input_file = $("#media-file"),
        send_button = $("#send-file"),
        upload_progress = $('<progress id="upload-progress" value="0" max="100" style="width: 179px"></progress>'),
        upload_percent = $("<span id='upload-percent' style='padding-left: 5px'>0%</span>");

    function resetProgress() {
        upload_progress[0].value = 0;
        upload_percent.text("0%");
    }

    function updateProgress(rpe) {
        var value = parseFloat(100 * rpe.loaded / rpe.total);
        upload_progress[0].value = value;
        upload_percent.text(parseInt(value, 10) + "%");
    }

    function uploadFinished(rpe, xhr) {
        updateProgress(rpe);
        upload_progress[0].value = 100;
        upload_percent.text("100%");

        var response = JSON.parse(xhr.responseText);

        $('#vitrine').html("<a href='"+response.vitrine.compare+"' target='_blank'><img width='100' height='100' src='"+response.vitrine.thumb+"' align='left'/> <b>"+response.vitrine.name+"</b> <br> a partir de R$"+response.vitrine.pricemin+"</a>");
        $('#upload-progress').remove();
    }

    function uploadFileHandler(e) {
        var opts, url, ad_id;

        e.preventDefault();

        $('#upload-progress').remove();
        input_file.parent().append(upload_progress);
        upload_percent.insertAfter(upload_progress);

        url = '/';

        opts = {
            url: url,
            files: input_file[0].files,
            onloadstart: resetProgress,
            onprogress: updateProgress,
            onload: uploadFinished
        };
        sendMultipleFiles(opts);
    }

    $('#send-file').click(uploadFileHandler);
});
