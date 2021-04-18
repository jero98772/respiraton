# Library
rm(list=ls())

if(!require(tidyverse)) install.packages('tidyverse')
if(!require(shiny)) install.packages('shiny')
if(!require(leaflet)) {
  devtools::install_github('rstudio/leaflet')
  devtools::install_github("rstudio/leaflet.providers")
  devtools::install_github('bhaskarvk/leaflet.extras')
}
if(!require(lubridate)) install.packages('lubridate')
if(!require(influxdbr)) install.packages('influxdbr')
if(!require(shinycssloaders)) install.packages('shinycssloaders')
if(!require(openair)) install.packages('openair')
if(!require(xts)) install.packages('xts')
if(!require(rgdal)) install.packages('rgdal')

#Loading Shape para parques

parques <- readOGR("www/parques_seleccionados.shp",
                  layer = "parques_seleccionados", GDAL1_integer64_policy = TRUE)

# Loading correspondencia de parques y canarios
parques_canarios <- read_csv("parques_canarios.csv",
                             col_types = cols(ID_PARQUE = col_character(),
                                              NOMBRE_PAR = col_character(), CODIGOPOT = col_skip(),
                                              TIPOPARQUE = col_character(), LOCNOMBRE = col_character(),
                                              Long = col_double(), Lat = col_double(),
                                              Canario = col_character()))

# Sites
Sites<-c(
  "PM2.5_BOG_FON_Hayuelos_E01",
  "PM2.5_BOG_CHA_Virrey_E01",
  "PM2.5_BOG_ENG_Tibabuyes_E08",
  "PM2.5_BOG_TUN_EstacionTunal",
  "PM2.5_BOG_TEU_Salitre_E02",
  "PM2.5_BOG_ENG_SML_E05",
  "PM2.5_BOG_ENG_EstacionFerias",
  "PM2.5_BOG_KEN_EstacionKennedy"
)


get_CanAirIO<-function(site,
                       days=500,
                       pollutant="pm25"){
  # Creating Connection file for inFlux
  conn<-influx_connection(host = "influxdb.canair.io")

  data<-data.frame(influx_select(con = conn,
                                 db = "canairio",
                                 measurement = paste0("\"",site,"\""),
                                 where = paste0("time >= now() - ",days,"d"),
                                 return_xts = FALSE,
                                 field_keys = paste0("time, ",pollutant),
                                 group_by = "*",simplifyList = TRUE))
  return(data)
}

# Para consultar la información del parque --------------------------------

ref_day1<-match(weekdays(force_tz(Sys.Date()-ifelse(hour(force_tz(Sys.time(),
                                                                  tzone = "America/Bogota"))<6,1,0),
                                  tzone = "America/Bogota"),abbreviate = TRUE),table = c("Mon","Tue","Wed","Thu","Fri","Sat","Sun"))

fut_day1<-c("Lunes","Martes","Miercoles","Jueves","Viernes","Sábado","Domingo")[ifelse(ref_day1==7,1,ref_day1+1)]


Forecast_update<-function(){
  # Process hourly medians
  DB_parques<-do.call(rbind,lapply(Sites, function(x){
    adj_day<-NULL

    tryCatch({

      data<-get_CanAirIO(x,days = 24)%>%
        select(time,pm25)%>%
        rename(date=time)%>%
        mutate(pm25=ifelse(pm25>1e5,NA,pm25)) # Readings above 1e5 are discarded
      # Procesa medias horarias de los datos
      qxts <- xts(data[,-1], order.by=data[,1])

      hqxts<-period.apply(qxts, endpoints(qxts, "hours"), mean,na.rm = TRUE)
      hqxts<-xts::align.time(hqxts,3600)

      summ_data<-data.frame(date=index(hqxts),pm25=coredata(hqxts))
      # Corre analisis de medias horarias de las ultimas tres semanas
      Observed_trends<-openair::timeVariation(summ_data,pollutant = "pm25",main=x,local.tz = "America/Bogota",)
      # Extrae los patrones diarios hora-a-hora y semanales dia-a-dia
      obs_hour<-Observed_trends$data$hour
      obs_day<-Observed_trends$data$day
      # Extrae fecha actual para pronostico
      date_for_adj <-force_tz(Sys.Date()-ifelse(hour(force_tz(Sys.time(),
                                                              tzone = "America/Bogota"))<6,1,0),
                              tzone = "America/Bogota")

      #Calculating the median for the current day or the day before if it is earlier than 6:00 am GMT-5
      ref_median<-median(summ_data$pm25[summ_data$date>date_for_adj])

      # Ajustar los patrones de acuerdo a valores observados
      if(hour(force_tz(Sys.time(),
                       tzone = "America/Bogota"))<6){

        ref_day<-match(weekdays(force_tz(Sys.Date()-ifelse(hour(force_tz(Sys.time(),
                                                                         tzone = "America/Bogota"))<6,1,0),
                                         tzone = "America/Bogota"),abbreviate = TRUE),table = c("Mon","Tue","Wed","Thu","Fri","Sat","Sun"))

        fut_day<-ifelse(ref_day==7,1,ref_day+1)


        obs_median_d2d<-obs_day$Mean[obs_day$wkday==fut_day]-obs_day$Mean[obs_day$wkday==ref_day]
        obs_median6h<-median(obs_hour$Mean)

        adj_day <- obs_hour%>%
          mutate(fore_con=(Mean-obs_median6h)+ref_median+obs_median_d2d)%>%
          ungroup%>%
          select(hour,fore_con)

      }else{
        obs_median6h<-median(obs_hour$Mean[obs_hour$hour<=6])
        adj_day <- obs_hour%>%
          mutate(fore_con=(Mean-obs_median6h)+ref_median)%>%
          ungroup%>%select(hour,fore_con)
      }
      adj_day$site<-x
      adj_day$fore_con<-round(adj_day$fore_con,1)
      adj_day$fore_con[adj_day$fore_con<0]<-0

      return(adj_day)
    },error = function(e) { print("FAILED")})

    print(paste(x))
    return(NULL)

  }))
}
DB_parques<-Forecast_update()

last_hour<-function(x){
  y<-get_CanAirIO(x,days = 1)%>%
    select(time,pm25)%>%
    rename(date=time)%>%
    filter(date>Sys.time()-3600)

  return(mean(y$pm25)%>%
           round(1))
}


# Para hacer el grafico del pronostico ------------------------------------
plot_pronostico<-function(x){
plot_data <- data.frame(
  hour=c(0:23),
  count=c(1)
)%>%left_join(DB_parques%>%filter(site==parques_canarios$Canario[parques_canarios$ID_PARQUE==x])%>%
                select(-site),by="hour")%>%
  mutate(IBOCA=case_when(fore_con<12~"A",
                         fore_con>=12&fore_con<26~"B",
                         fore_con>=26&fore_con<35~"C",
                         fore_con>=35&fore_con<20~"D"))

# Compute percentages
plot_data$fraction = 24*plot_data$count / sum(plot_data$count)

# Compute the cumulative percentages (top of each rectangle)
plot_data$ymax = cumsum(plot_data$fraction)

# Compute the bottom of each rectangle
plot_data$ymin = c(0, head(plot_data$ymax, n=-1))

# Make the plot
a<-ggplot(plot_data, aes(ymax=ymax, ymin=ymin, xmax=4, xmin=3, fill=IBOCA)) +
  geom_rect(aes(ymax=0, ymin=6, xmax=4, xmin=1),fill="blue",alpha=0.1)+
  geom_rect(aes(ymax=18, ymin=24, xmax=4, xmin=1),fill="blue",alpha=0.1)+
  geom_rect(aes(ymax=6, ymin=18, xmax=4, xmin=1),fill="lightblue",alpha=0.1)+
  geom_rect(col="white")+
  scale_fill_manual(values = c("Green","Yellow","Orange","Red"),drop=FALSE)+
  scale_y_continuous(breaks = c(1:24),labels = paste0(c(1:24),"h"))+
  coord_polar(theta = "y",start = pi)+
  labs(title = "Pronóstico de Calidad de Aire")+
  scale_x_continuous(labels = NULL,limits = c(0.5, 4))+theme_minimal()+
  theme(panel.grid.minor.y = element_blank(),axis.text.x = element_text(face = "bold"),legend.position = "none"
  )
return(a)}


# Trend  ------------------------------------------------------------------
plot_trend<-function(x){
y<-DB_parques%>%
  filter(site==parques_canarios$Canario[parques_canarios$ID_PARQUE==x])%>%
  select(-site)%>%
  ggplot(aes(x=hour,y=fore_con))+
  geom_line()+
  geom_hline(yintercept = 0,size=2)+
  theme_bw()+
  labs(x="Hora",
       y="PM2.5 ug/m3")+
  scale_x_continuous(breaks = seq(0,23,6))+
  theme(panel.grid.major.x = element_blank(),
        panel.grid.minor.x = element_blank())

return(y)

}
# Layout de la pagina -----------------------------------------------------


ui <- fluidPage(div(class="outer",


                    leafletOutput("map"),
                    absolutePanel(id = "controls", class = "panel panel-default", fixed = TRUE,
                                  draggable = TRUE, top = 60, left = "auto", right = 20, bottom = "auto",
                                  width = 330, height = "auto",
                                  h1("Aire al Parque"),
                                  p(em("Fuente de datos: Red de monitores de bajo costo CanairIO disponible en https://canair.io/")),
                                  br(),
                                  p(strong("Consulta de pronóstico")),
                                  p(paste("Haga clic sobre el parque de su interes para conocer el pronóstico del día ",format(fut_day1,format = "%d/%m/%Y"))),
                                  br(),
                                  plotOutput("Pronostico", width = 250, height = 250),
                                  img(src='legend.png'),
                                  br(),
                                  plotOutput("Trend", width = 250, height = 150),

                    ),
                    tags$head(tags$style("#map{height:100vh !important;}"))

))


# Server ------------------------------------------------------------------


server <- function(input, output, session) {
  output$map<-renderLeaflet({
    leaflet(parques) %>%
      addPolygons(layerId = ~ID_PARQUE,color = "#444444", weight = 1, smoothFactor = 0.5,
                  opacity = 0.6, fillOpacity = 0.5,
                  fillColor = "blue",
                  highlightOptions = highlightOptions(color = "white", weight = 2,
                                                      bringToFront = TRUE),label = ~NOMBRE_PAR)%>%
      addProviderTiles(providers$CartoDB.Positron, options = providerTileOptions(noWrap = TRUE) ) %>%
      fitBounds(-74.079,4.56,-74.065, 4.723) ## Bogotá
})

  popup_parque <- function(id, lat, lng) {
    tmp_parque <- parques_canarios[parques_canarios$ID_PARQUE == id,][1,]


    texto <- as.character(
      tagList(
        tags$h4(tmp_parque$NOMBRE_PAR),
        tags$br(),
        tags$strong(HTML(paste0("Media ultima hora (ug/m3): ",last_hour(tmp_parque$Canario)))),
        tags$br(),
        tags$strong(HTML(paste0("Localidad: ",tmp_parque$LOCNOMBRE))),
        tags$br(),
        tags$strong(HTML(paste0("Tipo: ",tmp_parque$TIPOPARQUE))),
        tags$br(),
        tags$h5(HTML(paste0("Sensor asociado: ",tmp_parque$Canario)))

      )
    )
    leafletProxy("map") %>% addPopups(lng, lat, texto)
  }

  observe({
    leafletProxy("map")
    event <- input$map_shape_click
    if (is.null(event))
      return()

    isolate({
      print(event)
      output$Pronostico <- renderPlot(plot_pronostico(event$id))
      output$Trend <- renderPlot(plot_trend(event$id))
      popup_parque(event$id,event$lat,event$lng)
    })
  })



  }

shinyApp(ui, server)
