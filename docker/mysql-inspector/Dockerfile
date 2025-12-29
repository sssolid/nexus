FROM mysql:8.0

ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=autocare
ENV MYSQL_CHARACTER_SET_SERVER=utf8
ENV MYSQL_COLLATION_SERVER=utf8_general_ci

# Disable binlog (inspection only)
RUN echo "[mysqld]\nskip-log-bin" > /etc/mysql/conf.d/disable-binlog.cnf
