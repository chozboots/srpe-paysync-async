CREATE TABLE stripe_general_info (
    user_id integer PRIMARY KEY,
    customer_id character varying(255) UNIQUE NOT NULL,
    payment_method character varying(255) NOT NULL,
    last4 character varying(4),
    expiration character varying(255),
    has_funds boolean,
    CONSTRAINT fk_stripe_general_info_user FOREIGN KEY (user_id)
        REFERENCES users (user_id) ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE stripe_session_info (
    user_id integer PRIMARY KEY,
    customer_id character varying(255) UNIQUE NOT NULL,
    token character varying(255),
    checkout_session boolean,
    checkout_link character varying(255),
    checkout_link_expires timestamp without time zone,
    payment_status character varying(255),
    CONSTRAINT fk_stripe_session_info_user FOREIGN KEY (user_id)
        REFERENCES users (user_id) ON UPDATE NO ACTION ON DELETE NO ACTION,
    CONSTRAINT fk_stripe_session_info_general FOREIGN KEY (customer_id)
        REFERENCES stripe_general_info (customer_id) ON UPDATE NO ACTION ON DELETE NO ACTION
);
