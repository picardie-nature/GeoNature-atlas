$(document).ready(function() {
      myDataTable("#tableCommunes");

});

function myDataTable(domid){
      $(domid).DataTable({
          bPaginate: true,
          "bAutoWidth": true,
          info:false,
          lengthChange: false,
          language:{ 
                search:         "Rechercher :",
                info: "_START_ sur _MAX_"
            }
          /*order:[[0,"desc"],[1,"desc"],[ 4, 'asc' ]],
          columnDefs: [
                { width: "35%" , targets: [3, 4]}

          ]*/
        });
}
