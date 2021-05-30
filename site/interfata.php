<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="interfata.css">
    <title>History Searchers</title>
    <style>
    
        .highlight
        {
            color:blue;
            text-decoration:underline;
            cursor: pointer;
        }
        
        .highlight .tooltiptext {
            visibility: hidden;
            width: 120px;
            background-color: black;
            color: #fff;
            
            border-radius: 6px;
            padding: 3px 0;

            /* Position the tooltip */
            position: absolute;
            z-index: 1;
        }

        .highlight:hover .tooltiptext {
            visibility: visible;
        }
        
    </style>
    <script>
    if ( window.history.replaceState ) {
    window.history.replaceState( null, null, window.location.href );
    }
</script>
</head>

<body>
    
    <h1>History Searchers</h1>
    <hr>
    <div class="intro">
        <h3>Indicatii:</h3>
        <p class="indicatii">Introduceti un film in campul de mai jos pentru a afisa descrierea cu expresiile temporale marcate corespunzator si polaritatea acestuia.</p>
		<p class="indicatii">O data afisata descrierea, pozitionand mouse-ul peste expresia temporala evidentiata, veti putea observa polaritatea propozitiei in care se regaseste aceasta.</p>
        <p class="indicatii">De asemenea, dand click pe butonul "Descarca fisier" veti descarca un fisier ce contine expresiile temporale din descriere.</p>
    </div>
    
    <div id="container">
    <form action="" method="POST" id="formular">
        <input type="text" id="srch" name="srch" list="datalist" placeholder=" numele filmului">
        <input type="submit" id="submit" name="submit" value="Cauta">
        <?php
            $user = 'root';
            $pass = '';
            $db = 'tiln';

            $db = new mysqli('localhost', $user, $pass, $db) or die("unable to connect");
        ?>
        <datalist id="datalist">
            <?php
            //fetch data from database
            $sql = "SELECT nume FROM tiln";
            $result = mysqli_query($db, $sql) or die("Error " . mysqli_error($db));
            while($row = mysqli_fetch_array($result)) { ?>
            <option value="<?php echo $row['nume']; ?>"><?php echo $row['nume']; ?></option>
            <?php } ?>
            
        </datalist>
        
        
        <div id="descriere" class="arata">
         <?php
           
            if ( isset( $_POST['submit'] ) ) {
                $film = $_POST['srch'];
                $sql = "SELECT id,descriere,expresii,sentiment,polexpresii FROM tiln WHERE nume='$film'";
                $query = mysqli_query($db, $sql); 
                $result = $query->fetch_assoc(); 
                $rezultat0 = $result['id'];
                $rezultat = $result['descriere'];
                $rezultat2 = $result['expresii'];
                $rezultat3 = $result['sentiment'];
                $rezultat4 = $result['polexpresii'];
                
                if($rezultat):?>
                    <style> .arata {visibility: visible;} </style>
                <?php endif;
                echo shell_exec("python exprtempfile.py ".$rezultat0." ");
                
                echo "<p id=\"paragraf\">" . $rezultat . "</p>";
                echo '<script>
                document.addEventListener( \'DOMContentLoaded\',function(){
                var searchpara=document.getElementById("descriere").innerHTML;
                searchpara=searchpara.toString();
                highlight_word(searchpara);	
                },false);
        
                function highlight_word(searchpara)
                { 
                var text="' . $rezultat2. '";
                var text2 = '.$rezultat4.';
                var res2 = text2.split(" + ");
                var res = text.split(" + ");
                var new_text=searchpara;
                for (i = 0; i < res.length; i++) {
                    var pattern=new RegExp("("+res[i]+")");
                    new_text=new_text.replace(pattern, "<span class=\'highlight\'>"+res[i]+" <span class=\"tooltiptext\">"+res2[i]+"</span></span>");
                    console.log(searchpara);
                    
                }
                document.getElementById("descriere").innerHTML=new_text;
                document.getElementById("temporale").innerHTML="Polaritatea descrierii: ' . $rezultat3 . '";
                
                }
            </script>';
            }
         
         ?>
        </div>

        <div id="temporale" class="arata"></div>
        <div id="buton" class="arata"><a href="output.txt" download="output.txt" id="csvfile">Descarca fisier</a></div>
        
         
    </form>
    
    </div>
        
    
</body>

</html>