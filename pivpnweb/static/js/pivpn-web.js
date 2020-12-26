table = $("#datatable").DataTable({
    "responsive": true,
    "paging": true,
    "lengthChange": false,
    "searching": true,
    "ordering": true,
    "info": true,
    "autoWidth": false,
    "pageLength": 7,
    dom: 'Bfrtip',
    buttons:[
    {
        text: 'Create user',
        className: 'btn btn-outline-dark',
        attr:
        {
            id: 'articulo-nuevo'
        },
        action: function ( e, dt, node, config )
        {
          //$('#modal-nuevo-articulo').modal('show')
        },
        init: function(api, node, config){
          $(node).removeClass('dt-button')
        }
    }],
    language:{
        "emptyTable":     "No connected users",
        "info":           "Showing _START_ to _END_ of _TOTAL_ connected users",
        "infoEmpty":      "Showing 0 to 0 of 0 connected users",
        "infoFiltered":   "(filtered from _MAX_ total connected users)",
        "lengthMenu":     "Show _MENU_ connected users",
        "zeroRecords":    "No matching connected users found",
    }
});