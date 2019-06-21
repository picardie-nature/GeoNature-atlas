$(document).ready(function() {
      myDataTable("#myTable");

});

function myDataTable(domid){
      $(domid).DataTable({
          bPaginate: false,
          "bAutoWidth": false,
          language:{ search:         "Filtrer :"},
          columnDefs: [
                { width: "35%" , targets: [3, 4]}

          ]
        });
}
