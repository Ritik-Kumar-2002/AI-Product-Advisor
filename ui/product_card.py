import streamlit as st

def render_productCard():
    with st.container(border=True):
        st.subheader('📦Product detail')
        image_col, info_col = st.columns([0.55, 0.45], gap='medium')

        with image_col:
            image_url  = st.session_state.get('image_url')
            if image_url:
                st.image(image_url, use_container_width=True)
            else: 
                st.write(image_url)
        with info_col:
            st.markdown(f'<span class="product-title">{st.session_state["product"].name}</span>', unsafe_allow_html=True)

            st.markdown(f'<span class="product-brand"> Brand: {st.session_state["product"].brand}</span>', unsafe_allow_html=True)  

            st.markdown(f'<span class="product-rating">⭐ {st.session_state["product"].rating}/5</span>', unsafe_allow_html=True)
            
            st.markdown(f"""
                <span class='price'>
                    {st.session_state["product"].price}
                </span>
            """, unsafe_allow_html=True)

            st.markdown(f"""
                <span class='old-price'>
                    {st.session_state["product"].original_price or ""}
                </span>
            """, unsafe_allow_html=True)

            st.markdown(f'<span class="discount">{st.session_state["product"].discount or ""}</span>', unsafe_allow_html=True)

            
        st.divider()

        # Product Features
        st.subheader('⭐ Key Features')

        for feature in st.session_state["product"].key_features:
            st.markdown(f'🟣 {feature}')
        
        st.divider()

        # Product Specification
        st.subheader('⚙️ Product Specifications')
        if st.session_state["product"].specs: 
            specific_data = [ {"specification": key, "Details": value} for key,value in  st.session_state["product"].specs.items()]
            st.table(specific_data)
        
        # Return Policy
        st.markdown(
            f"""
            <div style="
                background:#EEE8FF;
                padding:15px;
                border-radius:12px;
                margin-top:10px;
            ">
                <b style="color:#4525B5;">
                    🔄 Return Policy
                </b>
                <p style="color:#302064;margin-bottom:0;">
                    {st.session_state["product"].return_policy or 'Policy unavailable'}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )