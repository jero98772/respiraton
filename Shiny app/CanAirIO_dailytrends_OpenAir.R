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


# Process hourly medians
lapply(Sites, function(x){
  data<-get_CanAirIO(x,days = 21)%>%
    select(time,pm25)%>%
    rename(date=time)%>%
    mutate(pm25=ifelse(pm25>1e5,NA,pm25)) # Readings above 1e5 are discarded

  qxts <- xts(data[,-1], order.by=data[,1])

  hqxts<-period.apply(qxts, endpoints(qxts, "hours"), median,na.rm = TRUE)
  hqxts<-xts::align.time(hqxts,3600)

  summ_data<-data.frame(date=index(hqxts),pm25=coredata(hqxts))

  Observed_trends<-openair::timeVariation(summ_data,pollutant = "pm25",main=x,local.tz = "America/Bogota")
  obs_hour<-Observed_trends$data$hour
  obs_day<-Observed_trends$data$day

  date_for_adj <-force_tz(Sys.Date()-ifelse(hour(force_tz(Sys.time(),
                                                          tzone = "America/Bogota"))<6,1,0),
                          tzone = "America/Bogota")

  #Calculating the median for the current day or the day before if it is earlier than 6:00 am GMT-5
  ref_median<-median(summ_data$pm25[summ_data$date>date_for_adj])

  if(hour(force_tz(Sys.time(),
                   tzone = "America/Bogota"))<6){

    ref_day<-match(weekdays(force_tz(Sys.Date()-ifelse(hour(force_tz(Sys.time(),
                                             tzone = "America/Bogota"))<6,1,0),
             tzone = "America/Bogota"),abbreviate = TRUE),table = c("Mon","Tue","Wed","Thu","Fri","Sat","Sun"))

    fut_day<-ifelse(ref_day==7,1,ref_day+1)


    obs_median_d2d<-obs_day$Mean[obs_day$wkday==fut_day]-obs_day$Mean[obs_day$wkday==ref_day]
    obs_median6h<-median(obs_hour$Mean)

    adj_day <- obs_hour%>%
      mutate(rel_con=(Mean-obs_median6h)+ref_median+obs_median_d2d)%>%
      ungroup%>%
      select(hour,rel_con)

  }else{
    obs_median6h<-median(obs_hour$Mean[obs_hour$hour<=6])
    adj_day <- obs_hour%>%mutate(rel_con=(Mean-obs_median6h)+ref_median)%>%ungroup%>%select(hour,rel_con)
  }
  print(paste("Done ",x))
})



