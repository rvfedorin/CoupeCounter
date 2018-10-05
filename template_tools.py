import os


class CreateHtmlTemplate:
    def __init__(self):
        self.body = """        
<head>
    <link rel="stylesheet" type="text/css" href="css/style.css">
</head>
                """

    def create_body(self):
        self.body += f"""

        <body>
        <center>
        <div id="sheet">
        <strong>Профиль {self.prof}, {self.color}, {self.system}</strong><br><br>
        <div class="showLogoPar">
          <div class="showLogoWww">
            <img src="{self.pic_system}"  />
            <img src="{self.pic_profile}" />
          <p class="clr"></p>
          </div>
          <div class="showPar">
            <span>Высота проёма: {self.door_height}</span><br />
            <span>Ширина проёма: {self.opening_width}</span><br />
            <span>Количество дверей: {self.doors}</span><br />
            <span>Мест перекрытия: {self.overlaps}</span><br />
          </div>
        </div>
        <p class="bb"></p><br>
          <table id='counttable' cellspacing=0 cellpading=5>
            <tr> 
              <td class='rightborder'>Размер двери: </td>
              <td class='bb'><strong><i>2460 x 218мм. НУЖНА ФОРМУЛА</i></strong></td>
            </tr>
            <tr>
              <td class='rightborder'>Размер плиты 10мм: </td>
              <td class='bb'><strong>1199 x 179мм. - 7шт. НУЖНА ФОРМУЛА</strong></td>
            </tr>
            <tr>
              <td class='rightborder'>Размер зеркала (стекла) 4мм: </td>
              <td class='bb'><strong>1197 x 177мм. - 7шт. НУЖНА ФОРМУЛА</strong></td>
            </tr>
            <tr>
              <td  class='rightborder'>Длина вертикального профиля: </td>
              <td><strong>2460мм. НУЖНА ФОРМУЛА</strong></td>
            </tr>
            <tr>
              <td class='rightborder'>Длина горизонтального и межсекционного профиля: </td>
              <td><strong>164мм. НУЖНА ФОРМУЛА</strong></td>
            </tr>
            <tr>
              <td  class='rightborder'>Межсекционный профиль: </td>
              <td><strong>{self.bolt}</strong></td>
            </tr>
            <tr>
              <td class='rightborder'>Длина силиконового уплотнителя для зеркала:</td>
              <td><strong>19м.</strong></td>
            </tr>
          </table>
          <br>Размеры с учётом &laquo;шлегеля&raquo;, 34м<br><br>
          {self.table_doors_view}
          <br><br><p class="bb"></p><br>
          <div class="count-knop">
          <div class="knop-print" onclick="print_doc()"><a href="#">Печать</a></div>
          </div>
          """
        self.body += """
          <script type="text/javascript">
            function print_doc(){
            window.print() ;
            }
          </script>
          """

    def __call__(self, *args, **kwargs):
        self.body += '\n'
        self.body += args[0]

    def __str__(self):
        return self.body

    def save(self):
        with open('temp.html', 'w') as file:
            file.write(self.body)

    def open_calc(self):
        os.system("start temp.html")

