$(document).ready(function() {
    // Handle form submission via AJAX
    $("#searchForm").submit(function(event) {
        event.preventDefault();
        var searchvalue = $("#searchvalue").val();
        search(searchvalue)
     
    });

    function search(searchValue) {
        $("#student-table-body tr").each(function() {
            var studentName = $(this).find(".student-name").text().toLowerCase();
            var studentEmail = $(this).find(".student-email").text().toLowerCase();
            if (studentName.includes(searchValue.toLowerCase()) || studentEmail.includes(searchValue.toLowerCase())) {
                $(this).show(); 
            } else {
                $(this).hide(); 
            }
        });
    }

   //
    $('#year').change(function() {
        var selectedUrl = $(this).val();
        window.location.href = selectedUrl;
    });
});
