(function ($) {
  'use strict'

$('#example2').DataTable({
    "paging": true,
    "lengthChange": false,
    "searching": false,
    "ordering": true,
    "info": true,
    "autoWidth": false,
    "responsive": true,
    "ajax": 'http://127.0.0.1:7778/get_flows?dev_id=10',
 
  });
})(jQuery)