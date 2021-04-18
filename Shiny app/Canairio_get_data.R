
#' Extracting data of a site for a single pollutant
#'
#' @param site string with the name of the site
#' @param days number of days to be extracted from today
#' @param pollutant name of the variable in the sensor
#'
#' @return a dataframe with the data
#' @export
#'
#' @examples
#'
#' get_CanAirIO("PM25_Berlin_CanAirIO_v2",days=365, pollutant="pm25")

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


