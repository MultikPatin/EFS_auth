FROM postgres:${POSTGRES_VERSION}

ENV SRC_PATH '/app'
ENV APP_DIR 'src/auth'

WORKDIR $SRC_PATH

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY poetry.lock pyproject.toml ./
RUN apt update -y && adpt upgrade -y && apt install -y wget make

RUN cd /tmp \
    && wget "https://github.com/keithf4/pg_partman/archive/refs/heads/master.tar.gz" \
    # && echo "${PARTMAN_CHECKSUM} ${PARTMAN_VERSION}.tar.gz" | sha512sum --check \
    && export C_INCLUDE_PATH=/opt/bitnami/postgresql/include/:/opt/bitnami/common/include/ \
    && export LIBRARY_PATH=/opt/bitnami/postgresql/lib/:/opt/bitnami/common/lib/ \
    && export LD_LIBRARY_PATH=/opt/bitnami/postgresql/lib/:/opt/bitnami/common/lib/ \
    && tar zxf master.tar.gz && cd pg_partman-master\
    && make \
    && make install \
    && cd .. && rm -r pg_partman-


# ENTRYPOINT ["/bin/bash", "-c", "exec ${SRC_PATH}/${APP_DIR}/entrypoint.sh"]
