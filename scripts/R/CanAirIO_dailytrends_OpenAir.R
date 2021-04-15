# Library
library(openair)
library(tidyverse)

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
  data<-get_CanAirIO(x)%>%
    select(time,pm25)%>%
    rename(date=time)%>%
    mutate(pm25=ifelse(pm25>1e5,NA,pm25)) # Readings above 1e5 are discarded

  qxts <- xts(data[,-1], order.by=data[,1])

  hqxts<-period.apply(qxts, endpoints(qxts, "hours"), median,na.rm = TRUE)

  summ_data<-data.frame(date=index(hqxts),pm25=coredata(hqxts))

  png(units = "mm",width = 250,height = 130,res = 330,filename = paste0(x,".png"))
  openair::timeVariation(summ_data,pollutant = "pm25",main=x)
  dev.off()
})



