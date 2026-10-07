/**
 * Event listener: Persists active tab selection in local storage and restores active state on reload.
 */
$(function() {
    $('a[data-toggle="tab"]').on('show.bs.tab', function(e) {
        window.localStorage.setItem('activeTab', $(e.target).attr('href'));
    });
    var activeTab = window.localStorage.getItem('activeTab');
    if (activeTab) {
        $('a[href="' + activeTab + '"]').tab('show');
    }
});
