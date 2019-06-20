$(document).ready(function() {
      myDataTable("#myTable");

});

function myDataTable(domid){
      $(domid).DataTable({
          bPaginate: false,
          language:{ search:         "Filtrer :"}
        });
}
