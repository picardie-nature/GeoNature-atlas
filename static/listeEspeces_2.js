$(document).ready(function() {
      myDataTable("#myTable");

});

function myDataTable(domid){
      $(domid).DataTable({
          bPaginate: false,
          "bAutoWidth": false,
          language:{ search:         "Filtrer :"},
          order:[[0,"desc"],[1,"desc"],[ 4, 'asc' ]],
          columnDefs: [
                { width: "35%" , targets: [3, 4]}

          ]
        });
}
