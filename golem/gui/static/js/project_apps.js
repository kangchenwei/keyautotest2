
$(document).ready(function() {
    getApps(project);
    $('#appsTree').treed();
});


function getApps(projectName){
    $.ajax({
        url: "/project/get_apps/",
        data: {
            "project": projectName
        },
        dataType: 'json',
        type: 'POST',
        success: function(pages) {
            $("#appsTree").append(Project.newElementForm('.'));
            Project.loadTreeElements($("#appsTree"), pages.sub_elements, 'app');
        },
    });
}
